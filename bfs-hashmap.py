from collections import deque


# ==========================
# HASH MAP
# ==========================

class LocationMap:
    """
    Stores Nairobi locations using Python's built-in dictionary
    (Hash Table implementation).
    """

    def __init__(self):
        self.locations = {}

    def add_location(self, location):
        """Adds a location if it doesn't already exist."""
        if location not in self.locations:
            self.locations[location] = len(self.locations)

    def get_location_id(self, location):
        """Returns the ID of a location."""
        return self.locations.get(location)

    def get_locations(self):
        """Returns all stored locations."""
        return list(self.locations.keys())

    def display_locations(self):
        """Displays all locations and their IDs."""
        print("\nLocations:")
        for location, location_id in self.locations.items():
            print(f"{location_id}: {location}")


# ==========================
# BFS TRAVERSAL
# ==========================

def bfs(graph, start):
    """
    Performs Breadth-First Search traversal.

    Parameters:
        graph (dict): Graph represented as an adjacency list.
        start (str): Starting location.

    Returns:
        list: Order in which nodes were visited.
    """

    visited = set()
    queue = deque([start])
    traversal = []

    while queue:
        current = queue.popleft()

        if current not in visited:
            visited.add(current)
            traversal.append(current)

            for neighbour, _ in graph.get(current, []):
                if neighbour not in visited:
                    queue.append(neighbour)

    return traversal


# ==========================
# ROUTE EXISTENCE CHECK
# ==========================

def route_exists(graph, start, destination):
    """
    Checks whether a route exists between two locations.

    Parameters:
        graph (dict): Graph represented as an adjacency list.
        start (str): Starting location.
        destination (str): Destination location.

    Returns:
        bool: True if a route exists, otherwise False.
    """

    visited = set()
    queue = deque([start])

    while queue:
        current = queue.popleft()

        if current == destination:
            return True

        if current not in visited:
            visited.add(current)

            for neighbour, _ in graph.get(current, []):
                if neighbour not in visited:
                    queue.append(neighbour)

    return False


# ==========================
# TESTING
# ==========================

if __name__ == "__main__":

    # Example graph
    graph = {
        "CBD": [("Westlands", 5), ("Upper Hill", 3)],
        "Westlands": [("CBD", 5), ("Parklands", 2)],
        "Upper Hill": [("CBD", 3), ("Kilimani", 4)],
        "Parklands": [("Westlands", 2)],
        "Kilimani": [("Upper Hill", 4)]
    }

    # Hash Map
    location_map = LocationMap()

    for location in graph.keys():
        location_map.add_location(location)

    location_map.display_locations()

    print("\nBFS Traversal from CBD:")
    print(bfs(graph, "CBD"))

    print("\nRoute Exists (CBD -> Kilimani):")
    print(route_exists(graph, "CBD", "Kilimani"))

    print("\nRoute Exists (CBD -> Airport):")
    print(route_exists(graph, "CBD", "Airport"))