import os
import zipfile
import requests
import numpy as np
import math
import heapq
import json
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask.json.provider import JSONProvider
from numba import njit
from scipy.interpolate import splprep, splev
import geopandas as gpd
from shapely.geometry import Point, Polygon
from shapely.prepared import prep

from simulator.marinetime_data import simulate_maritime_data
from explainer.explain import get_path_explanation

# --- Setup and Configuration ---

# Custom JSON provider to handle NumPy types
class NumpyJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        kwargs.setdefault("default", self.default)
        return json.dumps(obj, **kwargs)

    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)

    def default(self, obj):
        if isinstance(obj, np.integer): return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        if isinstance(obj, np.bool_): return bool(obj)
        if isinstance(obj, np.ndarray): return obj.tolist()
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

app = Flask(__name__)
app.json = NumpyJSONProvider(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Constants
SPEED_SCALING = {"passenger ship": 20, "cargo ship": 15, "tanker": 10}
LAND_CACHE_FILE = 'land_polygons.pkl'
GRID_RESOLUTION = 0.5  # Use a coarser grid for global scale

# --- Geospatial Data Handling ---

def download_and_prepare_land_data():
    """Downloads and caches a global land dataset from Natural Earth."""
    if os.path.exists(LAND_CACHE_FILE):
        print("Loading cached land data...")
        # geopandas does not provide read_pickle; use pandas to load the pickled GeoDataFrame
        return pd.read_pickle(LAND_CACHE_FILE)

    print("Downloading land data (this will happen only once)...")
    # Use the public S3-hosted Natural Earth file (stable direct link)
    url = 'https://naturalearth.s3.amazonaws.com/10m_physical/ne_10m_land.zip'
    zip_path = 'ne_10m_land.zip'
    shapefile_path = 'ne_10m_land.shp'

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(zip_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall('.')
    
    print("Processing shapefile...")
    land_gdf = gpd.read_file(shapefile_path)
    land_gdf.to_pickle(LAND_CACHE_FILE)

    # Clean up downloaded files
    for ext in ['.zip', '.shp', '.shx', '.dbf', '.prj', '.cpg']:
        if os.path.exists('ne_10m_land' + ext):
            os.remove('ne_10m_land' + ext)

    return land_gdf

# Load land data on startup
land_geometries = download_and_prepare_land_data()
prepared_land_polygons = [prep(geom) for geom in land_geometries.geometry]

def create_land_mask(lon, lat):
    """Creates a land mask from the prepared GeoPandas geometries."""
    mask = np.zeros((len(lat), len(lon)), dtype=bool)
    for j, lat_val in enumerate(lat):
        for i, lon_val in enumerate(lon):
            point = Point(lon_val, lat_val)
            for prep_geom in prepared_land_polygons:
                if prep_geom.contains(point):
                    mask[j, i] = True
                    break
    return mask

# --- Utility and Pathfinding Functions ---

@njit
def haversine(lon1, lat1, lon2, lat2):
    R = 6371
    dlon = math.radians(lon2 - lon1)
    dlat = math.radians(lat2 - lat1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def find_nearest_index(lon_array, lat_array, lon_val, lat_val):
    lon_idx = np.abs(lon_array - lon_val).argmin()
    lat_idx = np.abs(lat_array - lat_val).argmin()
    return int(lon_idx), int(lat_idx)

def smooth_path(path_points, num_points=100):
    if len(path_points) < 4: return path_points
    path_points = np.array(path_points)
    tck, u = splprep([path_points[:, 0], path_points[:, 1]], s=1.0, k=3)
    u_new = np.linspace(u.min(), u.max(), num_points)
    x_new, y_new = splev(u_new, tck, der=0)
    smoothed = np.c_[x_new, y_new]
    # Ensure start and end points are precise
    smoothed[0], smoothed[-1] = path_points[0], path_points[-1]
    return smoothed.tolist()

def find_nearest_water_node(start_i, start_j, land_mask, num_lon, num_lat):
    if not land_mask[start_j, start_i]: return start_i, start_j
    search_radius = 1
    while search_radius < max(num_lon, num_lat):
        for i in range(start_i - search_radius, start_i + search_radius + 1):
            for j in range(start_j - search_radius, start_j + search_radius + 1):
                if 0 <= i < num_lon and 0 <= j < num_lat and not land_mask[j, i]:
                    return i, j
        search_radius += 1
    return None # No water node found

def a_star(start, end, lon, lat, land_mask, speed, swh, ws):
    num_lon, num_lat = len(lon), len(lat)
    start_lon, start_lat = lon[start[0]], lat[start[1]]
    end_lon, end_lat = lon[end[0]], lat[end[1]]

    open_set = [(0, start)]
    came_from, g_score = {}, { (i, j): np.inf for i in range(num_lon) for j in range(num_lat) }
    g_score[start] = 0
    f_score = {start: haversine(start_lon, start_lat, end_lon, end_lat)}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == end:
            path = []
            while current in came_from: path.append(current); current = came_from[current]
            path.append(start)
            return path[::-1]

        i, j = current
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < num_lon and 0 <= nj < num_lat and not land_mask[nj, ni]:
                neighbor = (ni, nj)
                base_dist = haversine(lon[i], lat[j], lon[ni], lat[nj])
                weather_factor = 1 + (0.1 * swh[nj, ni]) + (0.05 * ws[nj, ni])
                cost = base_dist * weather_factor
                tentative_g_score = g_score[current] + cost / speed
                if tentative_g_score < g_score.get(neighbor, np.inf):
                    came_from[neighbor], g_score[neighbor] = current, tentative_g_score
                    f_score[neighbor] = tentative_g_score + haversine(lon[ni], lat[nj], end_lon, end_lat)
                    if neighbor not in [item[1] for item in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return None

# --- Flask Route ---
@app.route('/optimize_route', methods=['POST'])
def optimize_route():
    data = request.json
    if not data: return jsonify({"error": "No data provided"}), 400
    ship_type, start_port, end_port, departure_date = data.get('shipType'), data.get('startPort'), data.get('endPort'), data.get('departureDate')
    if not all([ship_type, start_port, end_port, departure_date]): return jsonify({"error": "Missing required fields"}), 400

    try:
        # Define the grid for the entire world
        lon = np.arange(-180, 180.1, GRID_RESOLUTION)
        lat = np.arange(-90, 90.1, GRID_RESOLUTION)
        
        print("Generating maritime data...")
        maritime_data = simulate_maritime_data(lon, lat)
        
        print("Creating land mask...")
        land_mask = create_land_mask(lon, lat)
        
        start_i, start_j = find_nearest_index(lon, lat, start_port[0], start_port[1])
        end_i, end_j = find_nearest_index(lon, lat, end_port[0], end_port[1])

        print("Finding nearest water nodes...")
        valid_start = find_nearest_water_node(start_i, start_j, land_mask, len(lon), len(lat))
        valid_end = find_nearest_water_node(end_i, end_j, land_mask, len(lon), len(lat))

        if not valid_start or not valid_end:
            return jsonify({"error": "Start or end point is on land. Please select points in the water."}), 400

        print("Calculating optimal route with A*...")
        path = a_star(valid_start, valid_end, lon, lat, land_mask, SPEED_SCALING[ship_type.lower()], maritime_data['swh'], maritime_data['ws'])

        if not path: return jsonify({"error": "No viable route found. The destination may be unreachable."}), 404
        
        print("Smoothing path...")
        path_coords = [[lon[i], lat[j]] for i, j in path]
        final_path_points = [start_port] + (path_coords[1:-1] if len(path_coords) > 2 else []) + [end_port]
        smoothed_path = smooth_path(final_path_points)
        
        total_distance = sum(haversine(p1[0], p1[1], p2[0], p2[1]) for p1, p2 in zip(smoothed_path, smoothed_path[1:]))
        route_data = {"distance": total_distance, "num_steps": len(smoothed_path), "start_port": start_port, "end_port": end_port}
        maritime_data_summary = {k: v for k, v in maritime_data.items() if isinstance(v, (int, float, bool))}

        print("Generating explanation...")
        explanation = get_path_explanation(route_data, maritime_data_summary)
        
        return jsonify({"optimized_route": smoothed_path, "explanation": explanation, **route_data})

    except Exception as e:
        app.logger.error(f"Error in optimize_route: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)

