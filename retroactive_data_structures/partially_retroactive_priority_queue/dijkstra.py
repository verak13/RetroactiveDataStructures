from partially_retroactive_priority_queue import PartiallyRetroactivePriorityQueue


def calculate_distances_prpq(pq, graph, starting_vertex):
    time_counter = 10

    distances = {vertex: float('infinity') for vertex in graph}
    distances[starting_vertex] = 0

    pq.add_insert(0, 0, starting_vertex)
    while len(pq) > 0:
        current_distance, current_vertex = pq.get_min()
        pq.add_delete_min(time_counter)
        time_counter += 10

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                pq.add_insert(time_counter, distance, neighbor)
                time_counter += 10
        print(pq)

    print(pq)
    return distances


if __name__ == "__main__":
    prpq = PartiallyRetroactivePriorityQueue()

    example_graph = {
        'E': {'F': 20, 'D': 50, 'A': 10},
        'F': {'E': 20, 'A': 20, 'D': 30},
        'D': {'F': 30, 'E': 50, 'A': 30, 'B': 10, 'C': 50},
        'A': {'E': 10, 'F': 20, 'D': 30, 'B': 10},
        'B': {'A': 10, 'D': 10, 'C': 10},
        'C': {'D': 50, 'B': 10},
    }
    # {'E': 10, 'F': 20, 'D': 20, 'A': 0, 'B': 10, 'C': 20}

    distances = calculate_distances_prpq(prpq, example_graph, 'A')
    print(distances)
