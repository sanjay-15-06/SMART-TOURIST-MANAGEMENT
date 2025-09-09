# File: geofence.py
import math
from database import get_all_geofences

def is_inside_geofence(lat, lon):
    """
    Returns True if point is inside any geofence.
    """
    R = 6371000  # Earth radius in meters
    for gf in get_all_geofences():
        center_lat, center_lon, radius = gf[2], gf[3], gf[4]
        phi1 = math.radians(lat)
        phi2 = math.radians(center_lat)
        delta_phi = math.radians(center_lat - lat)
        delta_lambda = math.radians(center_lon - lon)
        a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
        c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        if distance <= radius:
            return True, gf[1]
    return False, None

if __name__ == "__main__":
    inside, zone = is_inside_geofence(20.5, 78.5)
    print("Inside geofence:", inside, "Zone:", zone)
