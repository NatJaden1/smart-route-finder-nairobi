import heapq

def dijkstra(graph, start, end):
    # Initialize distances to all nodes as infinity, except the start node
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    # Track the path sequence
    previous_nodes = {node: None for node in graph}
    
    # Priority Queue stores tuples of (current_distance, node)
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Stop early if the destination is reached
        if current_node == end:
            break
            
        # Skip if we already found a shorter path to this node
        if current_distance > distances[current_node]:
            continue
            
        # Explore neighboring roads
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            
            # Update path if a shorter route to the neighbor is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
                
    # Reconstruct the final route backwards
    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]
        
    # Return infinity and an empty list if no route exists
    if distances[end] == float('inf'):
        return float('inf'), [] 
        
    # Return the total distance and the sequential route
    return distances[end], path