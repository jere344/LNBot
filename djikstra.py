def dijkstra(paths_index, origin, target):

    nodes = (node for node in paths_index)

    unvisited = {node: None for node in nodes}
    visited = {}
    cursor = origin
    current_distance = (0, cursor)
    unvisited[cursor] = current_distance

    while True:
        for neighbour, distance in paths_index[cursor].items():
            if neighbour not in unvisited:
                continue

            new_distance = (
                current_distance[0] + distance,
                current_distance[1] + neighbour,
            )
            if not unvisited[neighbour] or unvisited[neighbour][0] > new_distance[0]:
                unvisited[neighbour] = new_distance

        visited[cursor] = current_distance
        unvisited.pop(cursor)

        if cursor == target:
            break

        candidates = [node for node in unvisited.items() if node[1]]
        try:
            cursor, current_distance = min(candidates, key=lambda x: x[1][0])
        except ValueError:
            return False

    return visited[target]


from math import inf

paths_index = {
    "A": {"B": 2, "C": 1},
    "B": {"A": 1, "E": inf},
    "C": {"A": 1, "D": 1},
    "D": {"C": 10, "E": 1},
    "E": {"B": 1, "D": 1, "F": 1},
    "F": {"G": 1},
    "G": {},
}

print(dijkstra(paths_index, "A", "E"))
