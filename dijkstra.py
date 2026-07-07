"""
dijkstra.py
Implements Dijkstra's Shortest Path Algorithm over dynamic edge weights.
Incorporates traffic multipliers based on real-world rush hour profiles.
"""
import heapq

def dijkstra(graph_dict, start, end, peak_hour=False):
    """
    Computes optimal paths using custom weight scaling.
    Time Complexity: O((V + E) log V) via Binary Heap.
    """
    # Track minimum cumulative travel times instead of static distances
    times = {node: float('inf') for node in graph_dict}
    times[start] = 0
    
    previous_nodes = {node: None for node in graph_dict}
    priority_queue = [(0.0, start)]
    
    # Store dynamic weights calculated during search execution
    calculated_edge_weights = {}

    while priority_queue:
        current_time, current_node = heapq.heappop(priority_queue)
        
        if current_node == end:
            break
            
        if current_time > times[current_node]:
            continue
            
        for neighbor, distance, speed_limit, is_traffic_prone in graph_dict[current_node]:
            # Dynamic Weight Modifier: Apply scaling if road is prone to heavy rush-hour traffic
            traffic_multiplier = 2.5 if (peak_hour and is_traffic_prone) else 1.0
            
            # Base travel time in minutes: (Distance / Speed) * 60
            base_time = (distance / speed_limit) * 60
            effective_time = base_time * traffic_multiplier
            
            new_cumulative_time = current_time + effective_time
            
            if new_cumulative_time < times[neighbor]:
                times[neighbor] = new_cumulative_time
                previous_nodes[neighbor] = current_node
                calculated_edge_weights[(current_node, neighbor)] = distance
                heapq.heappush(priority_queue, (new_cumulative_time, neighbor))
                
    # Path Reconstruction
    path = []
    current = end
    total_distance = 0.0
    
    while current is not None:
        path.insert(0, current)
        prev = previous_nodes[current]
        if prev is not None:
            total_distance += calculated_edge_weights.get((prev, current), 0.0)
        current = prev
        
    if times[end] == float('inf'):
        return float('inf'), 0.0, []
        
    return round(times[end], 1), round(total_distance, 2), path