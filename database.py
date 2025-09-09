# File: database.py
import sqlite3

DB_NAME = "tourist_safety_system.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Tourist info
    c.execute('''
        CREATE TABLE IF NOT EXISTS tourists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            digital_id TEXT UNIQUE NOT NULL,
            itinerary TEXT,
            emergency_contacts TEXT,
            latitude REAL,
            longitude REAL
        )
    ''')
    
    # Trips table (optional for multiple trips per tourist)
    c.execute('''
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tourist_id INTEGER,
            start_date TEXT,
            end_date TEXT,
            FOREIGN KEY(tourist_id) REFERENCES tourists(id)
        )
    ''')
    
    # Alerts (SOS, illegal zones, anomalies)
    c.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tourist_id INTEGER,
            type TEXT,
            description TEXT,
            latitude REAL,
            longitude REAL,
            timestamp TEXT,
            resolved INTEGER DEFAULT 0,
            FOREIGN KEY(tourist_id) REFERENCES tourists(id)
        )
    ''')
    
    # Geofences / high-risk zones
    c.execute('''
        CREATE TABLE IF NOT EXISTS geofences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            center_lat REAL,
            center_lon REAL,
            radius REAL,
            type TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# Tourist CRUD
def add_tourist(name, digital_id, itinerary="", emergency_contacts="", lat=None, lon=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tourists (name, digital_id, itinerary, emergency_contacts, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)",
              (name, digital_id, itinerary, emergency_contacts, lat, lon))
    conn.commit()
    conn.close()

def update_tourist_location(digital_id, lat, lon):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tourists SET latitude=?, longitude=? WHERE digital_id=?", (lat, lon, digital_id))
    conn.commit()
    conn.close()

def get_all_tourists():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM tourists")
    data = c.fetchall()
    conn.close()
    return data

# Alerts
def add_alert(tourist_id, type_, description, lat, lon, timestamp):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO alerts (tourist_id, type, description, latitude, longitude, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
              (tourist_id, type_, description, lat, lon, timestamp))
    conn.commit()
    conn.close()

def get_all_alerts():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM alerts")
    data = c.fetchall()
    conn.close()
    return data

# Geofences
def add_geofence(name, center_lat, center_lon, radius, type_="restricted"):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO geofences (name, center_lat, center_lon, radius, type) VALUES (?, ?, ?, ?, ?)",
              (name, center_lat, center_lon, radius, type_))
    conn.commit()
    conn.close()

def get_all_geofences():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM geofences")
    data = c.fetchall()
    conn.close()
    return data

if __name__ == "__main__":
    create_tables()
    print("Database initialized successfully.")
