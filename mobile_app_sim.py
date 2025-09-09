# File: mobile_app_sim.py
import random
from datetime import datetime
from database import get_all_tourists, update_tourist_location, add_alert

def simulate_location_update():
    tourists = get_all_tourists()
    for t in tourists:
        # Random walk simulation
        lat = t[5] if t[5] else 20 + random.random()
        lon = t[6] if t[6] else 78 + random.random()
        lat += random.uniform(-0.001, 0.001)
        lon += random.uniform(-0.001, 0.001)
        update_tourist_location(t[2], lat, lon)
    print("Locations updated.")

def send_sos(tourist_id, lat, lon):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    add_alert(tourist_id, "SOS", "Emergency Alert Triggered", lat, lon, timestamp)
    print(f"SOS alert sent for tourist {tourist_id} at ({lat},{lon})")

if __name__ == "__main__":
    simulate_location_update()
    tourists = get_all_tourists()
    if tourists:
        send_sos(tourists[0][0], tourists[0][5] or 20.5, tourists[0][6] or 78.5)
