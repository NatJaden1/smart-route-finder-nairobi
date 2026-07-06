"""
gui.py
Smart Route Finder - Tkinter GUI

Responsibilities (yours):
- Build the window, inputs, and results display
- Handle user interactions (button click, dropdown selection)
- Call the route-finding backend and show what it returns

INTEGRATION NOTE:
`find_route()` below is a STUB standing in for the real pathfinding
module. The agreed contract is:

    find_route(start: str, end: str) -> (route, distance_km, time_min)
        route        : list[str]  e.g. ["CBD", "Ngong Road", "Karen"]
        distance_km  : float
        time_min     : float or int
    Raises ValueError if no route exists.

Once a teammate delivers the real module (e.g. route_engine.py),
replace the stub with:
    from route_engine import find_route
and delete the fake version. Nothing else in this file needs to change,
as long as the signature matches.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random

# Fixed list of Nairobi locations for the dropdowns.
# Swap this for real map/graph node data once it's available.
LOCATIONS = [
    "CBD",
    "Westlands",
    "Kilimani",
    "Karen",
    "Parklands",
    "Ngara",
    "Upper Hill",
    "Lavington",
    "Indusrial Area",
    
]


def find_route(start: str, end: str):
    """
    STUB backend function — replace with the real pathfinder.

    Invents a plausible-looking route/distance/time so the UI can be
    fully built and tested before the real backend exists.
    """
    if start == end:
        raise ValueError("Start and destination are the same place.")

    others = [p for p in LOCATIONS if p not in (start, end)]
    via = random.choice(others) if others else None
    route = [start, via, end] if via else [start, end]

    distance_km = round(random.uniform(3, 25), 1)
    time_min = round(distance_km * random.uniform(2.5, 4.0))

    return route, distance_km, time_min


class SmartRouteApp(tk.Tk):
    """Main application window for the Smart Route Finder."""

    def __init__(self):
        super().__init__()
        self.title("Smart Route Finder - Nairobi")
        self.geometry("420x380")
        self.resizable(False, False)
        self._build_widgets()

    # ---------- UI construction ----------

    def _build_widgets(self):
        padding = {"padx": 10, "pady": 8}

        # --- Input section ---
        input_frame = ttk.LabelFrame(self, text="Trip details")
        input_frame.pack(fill="x", **padding)

        ttk.Label(input_frame, text="From:").grid(
            row=0, column=0, sticky="w", padx=8, pady=6
        )
        self.from_var = tk.StringVar()
        self.from_box = ttk.Combobox(
            input_frame, textvariable=self.from_var,
            values=LOCATIONS, state="readonly", width=22
        )
        self.from_box.grid(row=0, column=1, padx=8, pady=6)

        ttk.Label(input_frame, text="To:").grid(
            row=1, column=0, sticky="w", padx=8, pady=6
        )
        self.to_var = tk.StringVar()
        self.to_box = ttk.Combobox(
            input_frame, textvariable=self.to_var,
            values=LOCATIONS, state="readonly", width=22
        )
        self.to_box.grid(row=1, column=1, padx=8, pady=6)

        # --- Action button ---
        self.find_button = ttk.Button(
            self, text="Find Route", command=self.on_find_route
        )
        self.find_button.pack(pady=10)

        # --- Results section ---
        results_frame = ttk.LabelFrame(self, text="Results")
        results_frame.pack(fill="both", expand=True, **padding)

        ttk.Label(results_frame, text="Route:").grid(
            row=0, column=0, sticky="nw", padx=8, pady=6
        )
        self.route_text = tk.Text(
            results_frame, height=5, width=30, state="disabled", wrap="word"
        )
        self.route_text.grid(row=0, column=1, padx=8, pady=6)

        self.distance_var = tk.StringVar(value="—")
        ttk.Label(results_frame, text="Distance:").grid(
            row=1, column=0, sticky="w", padx=8, pady=6
        )
        ttk.Label(results_frame, textvariable=self.distance_var).grid(
            row=1, column=1, sticky="w", padx=8, pady=6
        )

        self.time_var = tk.StringVar(value="—")
        ttk.Label(results_frame, text="Travel time:").grid(
            row=2, column=0, sticky="w", padx=8, pady=6
        )
        ttk.Label(results_frame, textvariable=self.time_var).grid(
            row=2, column=1, sticky="w", padx=8, pady=6
        )

    # ---------- Event handling ----------

    def on_find_route(self):
        start = self.from_var.get()
        end = self.to_var.get()

        if not start or not end:
            messagebox.showerror(
                "Missing input", "Please choose both a start and end location."
            )
            return

        try:
            route, distance_km, time_min = find_route(start, end)
        except ValueError as e:
            messagebox.showerror("Route error", str(e))
            return

        self._display_results(route, distance_km, time_min)

    def _display_results(self, route, distance_km, time_min):
        self.route_text.config(state="normal")
        self.route_text.delete("1.0", tk.END)
        self.route_text.insert(tk.END, " -> ".join(route))
        self.route_text.config(state="disabled")

        self.distance_var.set(f"{distance_km} km")
        self.time_var.set(f"{time_min} min")