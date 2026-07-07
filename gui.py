"""
gui.py
Upgraded UI built entirely on customtkinter and tkintermapview.
Provides clear multi-pane window separations, Google Maps style tiles, 
and real-time street-snapping via the OSRM Routing API.
"""
import customtkinter as ctk
from tkintermapview import TkinterMapView
from tkinter import messagebox
import urllib.request
import json

from graph import get_graph, get_locations, get_coordinates, get_location_info
from dijkstra import dijkstra
from bfs_hashmap import route_exists

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SmartRouteApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nairobi Intelligent Transit Router")
        self.geometry("1100x650")
        
        self.graph_data = get_graph()
        self.locations = get_locations()
        self.coords = get_coordinates()
        
        # State trackers for resetting drawn items across calculations
        self.map_markers = []
        self.map_path = None

        self._arrange_layout_panes()

    def _arrange_layout_panes(self):
        # Base Configuration: 2-Column Split
        self.grid_columnconfigure(0, weight=0, minsize=340)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # LEFT COLUMN: INTERACTIVE INPUT PANEL
        # ==========================================
        self.sidebar = ctk.CTkFrame(self, width=340, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        lbl_title = ctk.CTkLabel(self.sidebar, text="Nairobi Transit Router", font=ctk.CTkFont(size=20, weight="bold"))
        lbl_title.pack(pady=(20, 20), padx=20)

        # Options Container Frame
        form_frame = ctk.CTkFrame(self.sidebar)
        form_frame.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(form_frame, text="Origin Point:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 2))
        self.from_box = ctk.CTkComboBox(form_frame, values=self.locations, width=260)
        self.from_box.pack(padx=15, pady=(0, 10))

        ctk.CTkLabel(form_frame, text="Destination Point:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 2))
        self.to_box = ctk.CTkComboBox(form_frame, values=self.locations, width=260)
        self.to_box.pack(padx=15, pady=(0, 15))

        # Dynamic Traffic Parameter Selector
        traffic_frame = ctk.CTkFrame(self.sidebar)
        traffic_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(traffic_frame, text="Traffic Conditions Profile", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        self.traffic_var = ctk.StringVar(value="offpeak")
        
        rb_offpeak = ctk.CTkRadioButton(traffic_frame, text="Standard Off-Peak (Free Flow)", variable=self.traffic_var, value="offpeak")
        rb_offpeak.pack(anchor="w", padx=25, pady=5)
        
        rb_rush = ctk.CTkRadioButton(traffic_frame, text="Rush Hour Peak (Multiplier applied)", variable=self.traffic_var, value="rush")
        rb_rush.pack(anchor="w", padx=25, pady=(5, 15))

        # Primary Calculation Trigger
        self.btn_compute = ctk.CTkButton(self.sidebar, text="Compute Optimal Route", font=ctk.CTkFont(size=14, weight="bold"), height=40, command=self.on_find_route)
        self.btn_compute.pack(fill="x", padx=15, pady=15)

        # Output Results Panel
        self.results_frame = ctk.CTkFrame(self.sidebar)
        self.results_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        ctk.CTkLabel(self.results_frame, text="Route Diagnostics", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.txt_route = ctk.CTkTextbox(self.results_frame, height=90, activate_scrollbars=True, wrap="word")
        self.txt_route.pack(fill="x", padx=15, pady=5)
        self.txt_route.insert("1.0", "Route path profile visualization window...")
        self.txt_route.configure(state="disabled")

        self.lbl_distance = ctk.CTkLabel(self.results_frame, text="Cumulative Distance: -", font=ctk.CTkFont(size=13))
        self.lbl_distance.pack(anchor="w", padx=15, pady=2)

        self.lbl_time = ctk.CTkLabel(self.results_frame, text="Estimated Travel Time: -", font=ctk.CTkFont(size=13))
        self.lbl_time.pack(anchor="w", padx=15, pady=(2, 15))

        # ==========================================
        # RIGHT COLUMN: MAP CANVAS INTERFACE
        # ==========================================
        self.map_frame = ctk.CTkFrame(self)
        self.map_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Instantiate Map Engine centered over Nairobi coordinates
        self.map_widget = TkinterMapView(self.map_frame, corner_radius=10)
        self.map_widget.pack(fill="both", expand=True, padx=5, pady=5)
        self.map_widget.set_position(-1.2833, 36.8219) 
        self.map_widget.set_zoom(13)
        
        # Enable clean Google Maps layer skin
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    def on_find_route(self):
        start = self.from_box.get()
        destination = self.to_box.get()
        is_rush = (self.traffic_var.get() == "rush")

        # Guard Rails & Input Validation
        if start == destination:
            messagebox.showerror("Invalid Routing Target", "Origin and Destination coordinates cannot overlap.")
            return

        if not route_exists(self.graph_data, start, destination):
            messagebox.showerror("Graph Error", "Target network cluster isolated. No valid path exists.")
            return

        # Clear existing visual graphics from canvas map
        for marker in self.map_markers:
            marker.delete()
        self.map_markers.clear()
        if self.map_path:
            self.map_path.delete()
            self.map_path = None

        # Execute Shortest Path Computation (Dijkstra)
        est_time, distance, route_sequence = dijkstra(self.graph_data, start, destination, peak_hour=is_rush)

        # Update Metrics Sidebar UI
        self.txt_route.configure(state="normal")
        self.txt_route.delete("1.0", "end")
        self.txt_route.insert("1.0", " -> ".join(route_sequence))
        self.txt_route.configure(state="disabled")

        self.lbl_distance.configure(text=f"Cumulative Distance: {distance} km")
        self.lbl_time.configure(text=f"Estimated Travel Time: {est_time} minutes")

        # Plot Spatial Map Node Markers
        for index, node in enumerate(route_sequence):
            node_coords = self.coords[node]
            info = get_location_info(node)
            marker_title = f"[{index+1}] {node}\n{info['category']}"
            
            # Color code critical nodes (Start, End vs Intermediate Waypoints)
            if index == 0:
                color = "#2ECC71"  # Emerald Green
            elif index == len(route_sequence) - 1:
                color = "#E74C3C"  # Alizarin Red
            else:
                color = "#3498DB"  # Peter River Blue

            new_marker = self.map_widget.set_marker(node_coords[0], node_coords[1], text=marker_title, marker_color_circle=color)
            self.map_markers.append(new_marker)

        # =============================================================
        # STREET-SNAPPING POLYLINE TRACKER via OSRM API
        # =============================================================
        path_coordinates = []
        try:
            # Format coordinate query string: "lng,lat;lng,lat;..."
            coord_string = ";".join([f"{self.coords[node][1]},{self.coords[node][0]}" for node in route_sequence])
            url = f"http://router.project-osrm.org/route/v1/driving/{coord_string}?overview=full&geometries=geojson"
            
            # Request route geometries from the public API
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            data = json.loads(response.read().decode())
            
            if data.get("code") == "Ok":
                # Extract road coordinate pairs
                geometry = data["routes"][0]["geometry"]["coordinates"]
                # Convert back from [lng, lat] to [lat, lng] format for mapping display
                path_coordinates = [(coord[1], coord[0]) for coord in geometry]
            else:
                # API failure fallback to straight lines
                path_coordinates = [self.coords[node] for node in route_sequence]
        except Exception:
            # General safe network catch fallback
            path_coordinates = [self.coords[node] for node in route_sequence]

        # Draw the snapped track layout across the map canvas
        path_color = "#E67E22" if is_rush else "#1ABC9C"
        self.map_path = self.map_widget.set_path(path_coordinates, color=path_color, width=4)
        
        # Recenter map window around the start node coordinates
        self.map_widget.set_position(self.coords[start][0], self.coords[start][1])