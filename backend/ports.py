import json
import os
import math
import csv
from typing import Dict, Tuple, Any, List, Optional

try:
    # KD-tree for fast nearest neighbor (optional dependency: scipy)
    from scipy.spatial import cKDTree
except Exception:
    cKDTree = None

BASE_DIR = os.path.dirname(__file__)
PORTS_JSON = os.path.join(BASE_DIR, 'data', 'ports.json')
PORTS_FULL_CSV = os.path.join(BASE_DIR, 'data', 'ports_full.csv')


def _haversine_km(lon1, lat1, lon2, lat2) -> float:
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2.0)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c


class PortsIndex:
    """Loads ports from either the small bundled JSON or a full CSV and
    provides a nearest-neighbor lookup. If a full CSV is present and SciPy
    is available, a KD-tree is used for fast queries.
    """
    def __init__(self):
        self.ports: List[Dict[str, Any]] = []
        self._tree: Optional[cKDTree] = None
        self._coords = None
        self._load()

    def _load(self):
        if os.path.exists(PORTS_FULL_CSV):
            self.ports = self._load_from_csv(PORTS_FULL_CSV)
        else:
            with open(PORTS_JSON, 'r', encoding='utf-8') as f:
                self.ports = json.load(f)

        # Build KD-tree if possible
        if cKDTree and len(self.ports) > 0:
            # Use (lat, lon) in radians projected to 3D unit sphere for good spherical NN
            coords = []
            for p in self.ports:
                lat_r = math.radians(float(p['lat']))
                lon_r = math.radians(float(p['lon']))
                x = math.cos(lat_r) * math.cos(lon_r)
                y = math.cos(lat_r) * math.sin(lon_r)
                z = math.sin(lat_r)
                coords.append((x, y, z))
            self._coords = coords
            self._tree = cKDTree(coords)

    @staticmethod
    def _load_from_csv(path: str) -> List[Dict[str, Any]]:
        ports = []
        with open(path, 'r', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            # Expect columns like: name,lat,lon,country,unlocode (case-insensitive)
            for row in reader:
                try:
                    lat = float(row.get('lat') or row.get('latitude') or row.get('LAT') or row.get('Latitude'))
                    lon = float(row.get('lon') or row.get('longitude') or row.get('LON') or row.get('Longitude'))
                except Exception:
                    continue
                ports.append({
                    'name': row.get('name') or row.get('Name') or row.get('port_name') or 'Unknown',
                    'lat': lat,
                    'lon': lon,
                    'country': row.get('country') or row.get('Country') or None,
                    'unlocode': row.get('unlocode') or row.get('UNLOCODE') or None,
                })
        return ports

    def find_nearest(self, lat: float, lon: float) -> Dict[str, Any]:
        if not self.ports:
            raise RuntimeError('No ports available')

        if self._tree is None:
            # fallback to linear scan
            best = None
            best_dist = float('inf')
            for p in self.ports:
                d = _haversine_km(lon, lat, p['lon'], p['lat'])
                if d < best_dist:
                    best_dist = d
                    best = p
            return {
                'name': best['name'],
                'country': best.get('country'),
                'unlocode': best.get('unlocode'),
                'lat': best['lat'],
                'lon': best['lon'],
                'distance_km': round(best_dist, 2)
            }

        # Use KD-tree on unit sphere; query for nearest neighbor(s)
        lat_r = math.radians(lat)
        lon_r = math.radians(lon)
        qx = math.cos(lat_r) * math.cos(lon_r)
        qy = math.cos(lat_r) * math.sin(lon_r)
        qz = math.sin(lat_r)
        dist, idx = self._tree.query((qx, qy, qz), k=1)
        # idx is index in ports
        p = self.ports[int(idx)]
        # compute accurate haversine distance
        d_km = _haversine_km(lon, lat, p['lon'], p['lat'])
        return {
            'name': p['name'],
            'country': p.get('country'),
            'unlocode': p.get('unlocode'),
            'lat': p['lat'],
            'lon': p['lon'],
            'distance_km': round(d_km, 2)
        }


# Single global index for module-level functions
_INDEX = None


def _ensure_index():
    global _INDEX
    if _INDEX is None:
        _INDEX = PortsIndex()
    return _INDEX


def find_nearest_port(lat: float, lon: float) -> Dict[str, Any]:
    idx = _ensure_index()
    return idx.find_nearest(lat, lon)