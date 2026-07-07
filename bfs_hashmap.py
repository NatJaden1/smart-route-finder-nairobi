"""
bfs_hashmap.py
Validates structural integrity, emulates custom mapping, and verifies path reachability.
"""
from collections import deque

class LocationMap:
    def __init__(self):
        self.locations = {}

    def add_location(self, location):
        if location not in self.locations:
            self.locations[location] = len(self.locations)

    def get_location_id(self, location):
        return self.locations.get(location)

    def get_locations(self):
        return list(self.locations.keys())


def route_exists(graph_dict, start, destination):
    """Performs a strict structural BFS validation to ensure a path exists."""
    if start not in graph_dict or destination not in graph_dict:
        return False
        
    visited = set()
    queue = deque([start])

    while queue:
        current = queue.popleft()

        if current == destination:
            return True

        if current not in visited:
            visited.add(current)
            for neighbor, _, _, _ in graph_dict.get(current, []):
                if neighbor not in visited:
                    queue.append(neighbor)
    return False