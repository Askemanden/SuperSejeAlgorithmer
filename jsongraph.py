import json
from typing import List, Tuple
Edge = Tuple[int, int, int]  # (source, destination, weight)
Graph = List[Edge]

def readData(file_path : str) -> Tuple[Graph, int]:
    with open(file_path, 'r') as file:
        data = json.load(file)
        graph = data["graph"]
        graph = [tuple(x) for x in graph]

        vertex_count = 0

        for source, destination, weight in graph:
            vertex_count = max(source+1, vertex_count)
            vertex_count = max(destination+1, vertex_count)

        print(graph)
        print(graph[0])
        print(vertex_count)
        return graph, vertex_count

if __name__ == "__main__":
    readData("graph.json")