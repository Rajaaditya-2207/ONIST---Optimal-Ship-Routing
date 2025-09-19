import numpy as np


def simulate_maritime_data(grid_lon, grid_lat, seed: int | None = None):
    """
    Generate randomized maritime data for a lon/lat grid.

    This produces arrays for:
      - 'swh' (significant wave height, meters)
      - 'ws'  (wind speed, knots)
      - 'u_surf' and 'v_surf' (surface current components, knots)

    The function uses spatially-varying random fields (Gaussian bumps + base
    background) so each call returns a different (but realistic-looking)
    pattern. Pass a `seed` to reproduce a specific realization.

    Args:
        grid_lon (sequence): 1D array-like of longitudes (degrees).
        grid_lat (sequence): 1D array-like of latitudes (degrees).
        seed (int|None): Optional RNG seed for reproducibility.

    Returns:
        dict: keys match what the backend expects (arrays are shaped
              (len(grid_lat), len(grid_lon))). Summary statistics are
              included for the explanation module.
    """
    rng = np.random.default_rng(seed)

    num_lon = len(grid_lon)
    num_lat = len(grid_lat)

    # Create coordinate matrices (lon across columns, lat across rows)
    LON, LAT = np.meshgrid(np.asarray(grid_lon), np.asarray(grid_lat))

    # --- Significant Wave Height (meters) ---
    # Base background waves between 0.2 and 1.2 m
    base_swh = rng.uniform(0.2, 1.2, size=(num_lat, num_lon))
    # Add a few random high-wave Gaussian patches
    num_patches = rng.integers(1, 4)
    lon_span = (np.max(grid_lon) - np.min(grid_lon)) or 1.0
    lat_span = (np.max(grid_lat) - np.min(grid_lat)) or 1.0
    for _ in range(num_patches):
        cx = rng.uniform(np.min(grid_lon), np.max(grid_lon))
        cy = rng.uniform(np.min(grid_lat), np.max(grid_lat))
        amp = rng.uniform(1.0, 3.5)  # meters above background
        sigma_lon = rng.uniform(0.05 * lon_span, 0.25 * lon_span)
        sigma_lat = rng.uniform(0.05 * lat_span, 0.25 * lat_span)
        bump = amp * np.exp(-(((LON - cx) ** 2) / (2 * sigma_lon ** 2) + ((LAT - cy) ** 2) / (2 * sigma_lat ** 2)))
        base_swh += bump

    swh = base_swh.astype(float)

    # --- Wind Speed (knots) ---
    base_ws = rng.uniform(3.0, 12.0, size=(num_lat, num_lon))
    # wind patches (stronger winds)
    num_wind_patches = rng.integers(1, 4)
    for _ in range(num_wind_patches):
        cx = rng.uniform(np.min(grid_lon), np.max(grid_lon))
        cy = rng.uniform(np.min(grid_lat), np.max(grid_lat))
        amp = rng.uniform(5.0, 20.0)
        sigma_lon = rng.uniform(0.05 * lon_span, 0.3 * lon_span)
        sigma_lat = rng.uniform(0.05 * lat_span, 0.3 * lat_span)
        bump = amp * np.exp(-(((LON - cx) ** 2) / (2 * sigma_lon ** 2) + ((LAT - cy) ** 2) / (2 * sigma_lat ** 2)))
        base_ws += bump

    ws = base_ws.astype(float)

    # --- Surface Currents (knots) ---
    # Create a gently varying current field with a dominant east/west banding
    # plus small random eddies
    lon_norm = (LON - np.min(grid_lon)) / (lon_span or 1.0)
    lat_norm = (LAT - np.min(grid_lat)) / (lat_span or 1.0)
    u_surf = 0.5 * np.sin(2 * np.pi * lat_norm)  # east/west banding
    v_surf = 0.2 * np.cos(2 * np.pi * lon_norm)  # north/south weak variation

    # Add small random noise/eddies
    u_surf += rng.normal(0.0, 0.2, size=(num_lat, num_lon))
    v_surf += rng.normal(0.0, 0.1, size=(num_lat, num_lon))

    u_surf = u_surf.astype(float)
    v_surf = v_surf.astype(float)

    # Summary statistics for explanations
    avg_swh = float(np.round(np.mean(swh), 2))
    avg_wind_speed = float(np.round(np.mean(ws), 2))
    avg_current_speed = float(np.round(np.mean(np.sqrt(u_surf ** 2 + v_surf ** 2)), 2))
    adverse_weather = bool(np.max(swh) > 3.0 or np.max(ws) > 25.0)

    return {
        'swh': swh,
        'ws': ws,
        'u_surf': u_surf,
        'v_surf': v_surf,
        'avg_swh': avg_swh,
        'avg_wind_speed': avg_wind_speed,
        'avg_current_speed': avg_current_speed,
        'adverse_weather': adverse_weather,
    }
