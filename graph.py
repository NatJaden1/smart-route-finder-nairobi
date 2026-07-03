"""
graph.py

This module stores the Nairobi road network using an adjacency list.
Each location is a vertex and every road is a weighted edge.
The weight represents the road distance in kilometres.
"""

graph = {

    "CBD": [
        ("Westlands", 5),
        ("Upper Hill", 3),
        ("Kilimani", 6)
    ],

    "Westlands": [
        ("CBD", 5),
        ("Parklands", 2),
        ("Lavington", 4)
    ],

    "Parklands": [
        ("Westlands", 2),
        ("Ngara", 3)
    ],

    "Ngara": [
        ("Parklands", 3),
        ("CBD", 2)
    ],

    "Upper Hill": [
        ("CBD", 3),
        ("Kilimani", 4),
        ("Industrial Area", 5)
    ],

    "Kilimani": [
        ("CBD", 6),
        ("Upper Hill", 4),
        ("Lavington", 3)
    ],

    "Lavington": [
        ("Westlands", 4),
        ("Kilimani", 3),
        ("Karen", 8)
    ],

    "Karen": [
        ("Lavington", 8),
        ("Langata", 5)
    ],

    "Langata": [
        ("Karen", 5),
        ("Industrial Area", 6)
    ],

    "Industrial Area": [
        ("Upper Hill", 5),
        ("Langata", 6)
    ]

}


def get_graph():
    """
    Returns the Nairobi road network.
    """
    return graph


def get_locations():
    """
    Returns all available locations.
    """
    return sorted(graph.keys())


def display_graph():
    """
    Prints the graph in a readable format.
    """
    for location, neighbours in graph.items():
        print(f"{location}: {neighbours}")

if __name__ == "__main__":
    display_graph()

# Dictionary storing additional information about each location

location_info = {
    "CBD": {
        "full_name": "Central Business District",
        "category": "Commercial",
        "description": "The main business and financial centre of Nairobi."
    },

    "Westlands": {
        "full_name": "Westlands",
        "category": "Commercial",
        "description": "A busy area known for offices, shopping malls, restaurants, and nightlife."
    },

    "Parklands": {
        "full_name": "Parklands",
        "category": "Residential",
        "description": "A residential area with schools, hospitals, and shopping centres."
    },

    "Ngara": {
        "full_name": "Ngara",
        "category": "Residential",
        "description": "A mixed residential and commercial neighbourhood close to the CBD."
    },

    "Upper Hill": {
        "full_name": "Upper Hill",
        "category": "Business District",
        "description": "A major financial district with corporate offices and hospitals."
    },

    "Kilimani": {
        "full_name": "Kilimani",
        "category": "Residential",
        "description": "A modern residential area with apartments, restaurants, and shopping centres."
    },

    "Lavington": {
        "full_name": "Lavington",
        "category": "Residential",
        "description": "An upscale residential neighbourhood known for quiet estates."
    },

    "Karen": {
        "full_name": "Karen",
        "category": "Residential",
        "description": "A leafy suburb famous for spacious homes, attractions, and nature."
    },

    "Langata": {
        "full_name": "Langata",
        "category": "Residential",
        "description": "A suburban area near Nairobi National Park and several schools."
    },

    "Industrial Area": {
        "full_name": "Industrial Area",
        "category": "Industrial",
        "description": "The main manufacturing and industrial zone of Nairobi."
    }
}

def get_location_info(location):
    """
    Returns information about a specific location.
    """
    return location_info.get(location, "Location not found.")
