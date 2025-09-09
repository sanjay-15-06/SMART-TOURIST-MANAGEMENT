# File: ai_module.py
import random
from datetime import datetime
from database import get_all_tourists, add_alert

def detect_anomalies():
    tourists = get_all_tourists()
    for t in tourists:
        # 10% chance of anomaly
        if random.random() < 0.1:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            add_alert(t[0], "Anomaly", "Unusual behavior detected", t[5] or 20, t[6] or 78, timestamp)
            print(f"Anomaly detected for tourist {t[1]}")

if __name__ == "__main__":
    detect_anomalies()
