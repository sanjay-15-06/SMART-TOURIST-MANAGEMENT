# File: dashboard.py
import sys
import folium
import io
from PyQt5 import QtWidgets, QtWebEngineWidgets
from database import get_all_tourists, get_all_alerts, get_all_geofences

class DashboardApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tourist Safety Dashboard")
        self.setGeometry(100, 100, 1200, 800)
        self.layout = QtWidgets.QVBoxLayout(self)
        
        # Map view
        self.webview = QtWebEngineWidgets.QWebEngineView()
        self.layout.addWidget(self.webview)
        
        # Refresh button
        self.refresh_btn = QtWidgets.QPushButton("Refresh Map")
        self.refresh_btn.clicked.connect(self.update_map)
        self.layout.addWidget(self.refresh_btn)
        
        self.update_map()
    
    def update_map(self):
        base_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
        
        # Geofences
        for gf in get_all_geofences():
            folium.Circle(location=[gf[2], gf[3]], radius=gf[4], color='red', fill=True, fill_opacity=0.2,
                          popup=f"{gf[1]} ({gf[5]})").add_to(base_map)
        
        # Tourists
        for t in get_all_tourists():
            folium.Marker([t[5] or 20, t[6] or 78], popup=f"{t[1]} ({t[2]})",
                          icon=folium.Icon(color='blue')).add_to(base_map)
        
        # Alerts
        for a in get_all_alerts():
            folium.Marker([a[4], a[5]], popup=f"{a[2]}: {a[3]}", icon=folium.Icon(color='red')).add_to(base_map)
        
        data = io.BytesIO()
        base_map.save(data, close_file=False)
        self.webview.setHtml(data.getvalue().decode())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = DashboardApp()
    win.show()
    sys.exit(app.exec_())
