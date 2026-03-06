from typing import List, Tuple


Edge = Tuple[int, int, int]  # (source, destination, weight)
Graph = List[Edge]


class DisjointSetUnion:
    def __init__(self, number_of_vertices: int) -> None:
        self.parent: List[int] = list(range(number_of_vertices))
        self.rank: List[int] = [1] * number_of_vertices

    def find(self, vertex: int) -> int:
        if self.parent[vertex] != vertex:
            self.parent[vertex] = self.find(self.parent[vertex])
        return self.parent[vertex]

    def union(self, vertex_a: int, vertex_b: int) -> bool:
        root_a = self.find(vertex_a)
        root_b = self.find(vertex_b)

        if root_a == root_b:
            return False

        if self.rank[root_a] < self.rank[root_b]:
            self.parent[root_a] = root_b
        elif self.rank[root_a] > self.rank[root_b]:
            self.parent[root_b] = root_a
        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1

        return True


def process_single_edge(
    edge: Edge,
    dsu: DisjointSetUnion,
    minimum_spanning_tree_edges: Graph,
    current_total_cost: int
) -> Tuple[int, bool]:
    """
    Determines whether or not an edge should be added to the mst and adds it if it should be. Modifies minimum_spanning_tree_edges
    
    :param edge: Edge to decide if should be added to MST
    :type edge: Edge
    :param dsu: Disjoing set union for the graph
    :type dsu: DisjointSetUnion
    :param minimum_spanning_tree_edges: The current minimum spanning tree of the graph. Modified by the function
    :type minimum_spanning_tree_edges: Graph
    :param current_total_cost: Current sum of weights of all included edges in the mst
    :type current_total_cost: int
    :return: The current totalt cost and whether or not an edge was added
    :rtype: Tuple[int, bool]
    """
    source, destination, weight = edge

    if dsu.find(source) != dsu.find(destination):
        dsu.union(source, destination)
        minimum_spanning_tree_edges.append(edge)
        return current_total_cost + weight, True

    return current_total_cost, False


def kruskal_minimum_spanning_tree(
    vertex_count: int,
    edges: Graph
) -> Tuple[int, Graph]:
    edges_sorted: Graph = sorted(edges, key=lambda e: e[2])

    dsu = DisjointSetUnion(vertex_count)
    minimum_spanning_tree_edges: List[Edge] = []
    total_cost: int = 0

    for edge in edges_sorted:
        total_cost, edge_added = process_single_edge(
            edge, dsu,minimum_spanning_tree_edges, total_cost
        )

        # FOR RUNNING VISUALIZATION USE SAME FUNCTION AND INSERT VISUALIZATION HERE

        if len( minimum_spanning_tree_edges) == vertex_count - 1:
            break

    return total_cost,minimum_spanning_tree_edges

if __name__ == "__main__":
    edges: Graph = [
    (0, 1, -3),
    (1, 3, 15),
    (2, 3, 4),
    (2, 0, 6),
    (0, 3, 5)
]

    cost, mst = kruskal_minimum_spanning_tree(4, edges)
    print("MST cost:", cost)
    print("Edges:", mst)
