import numpy as np

def simulate_maritime_data(grid_lon, grid_lat):
    """
    Generates a simulated grid of maritime data.

    In a real-world application, this function would fetch and process
    real-time data from sources like NOAA, Copernicus, etc.

    Args:
        grid_lon (np.array): Array of longitude points for the grid.
        grid_lat (np.array): Array of latitude points for the grid.

    Returns:
        dict: A dictionary containing grids for wave height, wind speed,
              and ocean currents (u and v components).
    """
    num_lon = len(grid_lon)
    num_lat = len(grid_lat)

    # Simulate Significant Wave Height (SWH) - gentle waves with a high-wave area
    swh = np.random.uniform(0.5, 1.5, size=(num_lat, num_lon))
    # Add a patch of rough seas
    swh[num_lat//4 : num_lat//2, num_lon//4 : num_lon//2] *= 3

    # Simulate Wind Speed (WS) in knots
    ws = np.random.uniform(5, 15, size=(num_lat, num_lon))
    # Add an area of high winds
    ws[num_lat//2 : 3*num_lat//4, num_lon//2 : 3*num_lon//4] *= 2.5

    # Simulate Ocean Currents (U and V components) in knots
    # Gentle eastward current in the south, westward in the north
    v_surf = np.zeros((num_lat, num_lon)) # North-South component
    u_surf = np.ones((num_lat, num_lon)) * 0.5 # East-West component
    u_surf[num_lat//2:, :] = -0.5 # Westward current in the northern half

    return {
        'swh': swh,
        'ws': ws,
        'v_surf': v_surf,
        'u_surf': u_surf,
        # For the explanation model
        'avg_swh': round(np.mean(swh), 2),
        'avg_wind_speed': round(np.mean(ws), 2),
        'avg_current_speed': round(np.mean(np.sqrt(u_surf**2 + v_surf**2)), 2),
        'adverse_weather': np.max(swh) > 3 or np.max(ws) > 25,
    }
