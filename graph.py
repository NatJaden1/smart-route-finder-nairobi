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


print(display_graph())

if __name__ == "__main__":
    display_graph()

