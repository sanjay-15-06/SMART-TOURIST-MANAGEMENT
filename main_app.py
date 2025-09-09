    # File: main_app.py
import sys
import folium, io, random
from PyQt5 import QtWidgets, QtWebEngineWidgets, QtCore
from datetime import datetime
from database import create_tables, add_tourist, get_all_tourists, update_tourist_location, add_alert, get_all_alerts, add_geofence, get_all_geofences
from blockchain import add_block, verify_id
from geofence import is_inside_geofence
from ai_module import detect_anomalies

create_tables()

# ----------------------- Background Worker -----------------------
class BackgroundWorker(QtCore.QThread):
    update_signal = QtCore.pyqtSignal()
    
    def run(self):
        while True:
            # 1. Update locations (simulate movement)
            tourists = get_all_tourists()
            for t in tourists:
                lat = t[5] if t[5] else 20 + random.random()
                lon = t[6] if t[6] else 78 + random.random()
                lat += random.uniform(-0.001, 0.001)
                lon += random.uniform(-0.001, 0.001)
                update_tourist_location(t[2], lat, lon)
                
                # 2. Check illegal zone
                inside, zone = is_inside_geofence(lat, lon)
                if inside:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    add_alert(t[0], "Illegal Zone", f"Entered {zone}", lat, lon, timestamp)
                
                # 3. Random SOS (10% chance)
                if random.random() < 0.05:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    add_alert(t[0], "SOS", "Emergency Triggered", lat, lon, timestamp)
            
            # 4. AI Anomaly Detection
            detect_anomalies()
            
            self.update_signal.emit()  # Signal GUI to refresh map
            self.sleep(5)  # Update every 5 seconds

# ----------------------- Main Application -----------------------
class TouristSafetyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Tourist Safety Monitoring")
        self.setGeometry(50, 50, 1300, 900)
        self.layout = QtWidgets.QVBoxLayout(self)
        
        # Map view
        self.webview = QtWebEngineWidgets.QWebEngineView()
        self.layout.addWidget(self.webview)
        
        # Alerts table
        self.alert_table = QtWidgets.QTableWidget()
        self.alert_table.setColumnCount(6)
        self.alert_table.setHorizontalHeaderLabels(["Tourist ID","Type","Description","Lat","Lon","Timestamp"])
        self.layout.addWidget(self.alert_table)
        
        # Control buttons
        self.button_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.button_layout)
        
        self.add_tourist_btn = QtWidgets.QPushButton("Register Tourist")
        self.add_tourist_btn.clicked.connect(self.register_tourist)
        self.button_layout.addWidget(self.add_tourist_btn)
        
        self.add_geofence_btn = QtWidgets.QPushButton("Add Geofence")
        self.add_geofence_btn.clicked.connect(self.add_geofence)
        self.button_layout.addWidget(self.add_geofence_btn)
        
        self.refresh_btn = QtWidgets.QPushButton("Refresh Map")
        self.refresh_btn.clicked.connect(self.update_map)
        self.button_layout.addWidget(self.refresh_btn)
        
        # Start background worker
        self.worker = BackgroundWorker()
        self.worker.update_signal.connect(self.update_map)
        self.worker.start()
        
        self.update_map()
    
    # ---------------- GUI Methods ----------------
    def register_tourist(self):
        name, ok1 = QtWidgets.QInputDialog.getText(self, "Tourist Name", "Enter tourist name:")
        if not ok1 or not name:
            return
        digital_id, ok2 = QtWidgets.QInputDialog.getText(self, "Digital ID", "Enter digital ID:")
        if not ok2 or not digital_id:
            return
        itinerary, ok3 = QtWidgets.QInputDialog.getText(self, "Trip Itinerary", "Enter itinerary:")
        if not ok3: itinerary = ""
        emergency, ok4 = QtWidgets.QInputDialog.getText(self, "Emergency Contacts", "Enter contacts:")
        if not ok4: emergency = ""
        
        add_tourist(name, digital_id, itinerary, emergency)
        add_block(digital_id, name, itinerary, emergency)
        QtWidgets.QMessageBox.information(self, "Success", f"Tourist {name} registered with blockchain ID!")
        self.update_map()
    
    def add_geofence(self):
        name, ok1 = QtWidgets.QInputDialog.getText(self, "Geofence Name", "Enter zone name:")
        if not ok1 or not name: return
        lat, ok2 = QtWidgets.QInputDialog.getDouble(self, "Latitude", "Enter center latitude:", decimals=6)
        if not ok2: return
        lon, ok3 = QtWidgets.QInputDialog.getDouble(self, "Longitude", "Enter center longitude:", decimals=6)
        if not ok3: return
        radius, ok4 = QtWidgets.QInputDialog.getDouble(self, "Radius (meters)", "Enter radius:", decimals=2)
        if not ok4: return
        add_geofence(name, lat, lon, radius, type_="restricted")
        QtWidgets.QMessageBox.information(self, "Success", f"Geofence {name} added!")
        self.update_map()
    
    def update_map(self):
        base_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
        
        # Add geofences
        for gf in get_all_geofences():
            folium.Circle(location=[gf[2], gf[3]], radius=gf[4], color='red', fill=True, fill_opacity=0.2,
                          popup=f"{gf[1]} ({gf[5]})").add_to(base_map)
        
        # Add tourists
        for t in get_all_tourists():
            folium.Marker([t[5] or 20, t[6] or 78], popup=f"{t[1]} ({t[2]})", icon=folium.Icon(color='blue')).add_to(base_map)
        
        # Add alerts
        alerts = get_all_alerts()
        self.alert_table.setRowCount(len(alerts))
        for i, a in enumerate(alerts):
            self.alert_table.setItem(i,0,QtWidgets.QTableWidgetItem(str(a[1])))
            self.alert_table.setItem(i,1,QtWidgets.QTableWidgetItem(a[2]))
            self.alert_table.setItem(i,2,QtWidgets.QTableWidgetItem(a[3]))
            self.alert_table.setItem(i,3,QtWidgets.QTableWidgetItem(str(a[4])))
            self.alert_table.setItem(i,4,QtWidgets.QTableWidgetItem(str(a[5])))
            self.alert_table.setItem(i,5,QtWidgets.QTableWidgetItem(a[6]))
            # Add to map
            folium.Marker([a[4], a[5]], popup=f"{a[2]}: {a[3]}", icon=folium.Icon(color='red')).add_to(base_map)
        
        data = io.BytesIO()
        base_map.save(data, close_file=False)
        self.webview.setHtml(data.getvalue().decode())

# ---------------- Main ----------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TouristSafetyApp()
    window.show()
    sys.exit(app.exec_())
