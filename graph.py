"""
graph.py
Stores accurate geographic coordinates and metadata for major Nairobi hubs.
Fixes routing anomalies (e.g., ensuring CBD -> Parklands does not detour via Kilimani).
"""

# Hardcoded geographic coordinates for interactive map rendering
COORDINATES = {
    "CBD": (-1.2833, 36.8219),
    "Ngara": (-1.2747, 36.8242),
    "Parklands": (-1.2612, 36.8122),
    "Westlands": (-1.2642, 36.8026),
    "Lavington": (-1.2745, 36.7694),
    "Kilimani": (-1.2912, 36.7874),
    "Upper Hill": (-1.2965, 36.8130),
    "Industrial Area": (-1.3115, 36.8524),
    "Langata": (-1.3262, 36.7884),
    "Karen": (-1.3201, 36.7050)
}

# Explicit Graph Adjacency List: (Neighbor, Base_Distance_KM, Speed_Limit_KMH, Is_Traffic_Prone_Road)
# Boolean flag marks notorious bottlenecks like Uhuru Hwy, Thika Rd, Ngong Rd, or Mombasa Rd.
graph = {
    "CBD": [
        ("Westlands", 4.0, 50, True),
        ("Upper Hill", 2.5, 40, False),
        ("Ngara", 2.0, 50, True)
    ],
    "Westlands": [
        ("CBD", 4.0, 50, True),
        ("Parklands", 2.0, 40, False),
        ("Lavington", 4.2, 50, False)
    ],
    "Parklands": [
        ("Westlands", 2.0, 40, False),
        ("Ngara", 2.8, 40, False)
    ],
    "Ngara": [
        ("Parklands", 2.8, 40, False),
        ("CBD", 2.0, 50, True)
    ],
    "Upper Hill": [
        ("CBD", 2.5, 40, False),
        ("Kilimani", 3.2, 40, False),
        ("Industrial Area", 4.5, 50, True)
    ],
    "Kilimani": [
        ("Upper Hill", 3.2, 40, False),
        ("Lavington", 3.0, 50, False),
        ("Langata", 5.5, 60, True)
    ],
    "Lavington": [
        ("Westlands", 4.2, 50, False),
        ("Kilimani", 3.0, 50, False),
        ("Karen", 8.5, 60, False)
    ],
    "Karen": [
        ("Lavington", 8.5, 60, False),
        ("Langata", 6.0, 60, False)
    ],
    "Langata": [
        ("Karen", 6.0, 60, False),
        ("Kilimani", 5.5, 60, True),
        ("Industrial Area", 7.0, 50, True)
    ],
    "Industrial Area": [
        ("Upper Hill", 4.5, 50, True),
        ("Langata", 7.0, 50, True)
    ]
}

location_info = {
    "CBD": {"full_name": "Central Business District", "category": "Commercial Hub", "description": "The administrative center of Nairobi."},
    "Westlands": {"full_name": "Westlands District", "category": "Commercial/Entertainment", "description": "Vibrant business hub north-west of CBD."},
    "Parklands": {"full_name": "Parklands Estate", "category": "Residential/Medical", "description": "Affluent community and primary hospital zone."},
    "Ngara": {"full_name": "Ngara Area", "category": "Mixed Residential", "description": "Key transit neighborhood bordering the northern CBD edge."},
    "Upper Hill": {"full_name": "Upper Hill Corporate District", "category": "Financial District", "description": "Hosts multi-national headquarters and skyscrapers."},
    "Kilimani": {"full_name": "Kilimani Estate", "category": "Mixed Urban Residential", "description": "Rapidly growing corporate residential zone west of CBD."},
    "Lavington": {"full_name": "Lavington Suburb", "category": "High-End Residential", "description": "Leafy suburban neighborhood with high-class zoning."},
    "Karen": {"full_name": "Karen Suburb", "category": "Exclusive Residential", "description": "Expansive green spaces and historic properties."},
    "Langata": {"full_name": "Langata Suburb", "category": "Residential/Tourism", "description": "Borders the Nairobi National Park and tourist circuits."},
    "Industrial Area": {"full_name": "Nairobi Industrial Area", "category": "Manufacturing Sector", "description": "The center of processing and logistics."}
}

def get_graph(): return graph
def get_locations(): return sorted(graph.keys())
def get_coordinates(): return COORDINATES
def get_location_info(loc): return location_info.get(loc, "Location missing from database.")