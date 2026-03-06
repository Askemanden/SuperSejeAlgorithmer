from kruskal import *
import pygame as pg
from typing import List, Tuple
import math

Edge = Tuple[int, int, int]  # (source, destination, weight)
Graph = List[Edge]



def drawGraphWithMST(graph: Graph, mst: Graph, vertex_count: int, surface: pg.Surface) -> None:
    """
    Draws a graph and shows which edges are in the current mst version
    
    :param graph: Graph to draw
    :type graph: Graph
    :param mst: MST to draw on top of graph
    :type mst: Graph
    :param vertex_count: Number of vertices in graph. It is assumed that vertices are numbered from 0 to vertex_count-1
    :type vertex_count: int
    :param surface: Surface to draw on
    :type surface: pg.Surface
    """

    circle_radius = 18

    surface_width, surface_height = surface.get_size()
    center_x, center_y = surface_width // 2, surface_height // 2
    layout_radius = min(surface_width, surface_height) // 3
    font = pg.font.SysFont("Times New Roman", 24)

    vertex_positions : List[Tuple[int,int]]= []
    for vertex_index in range(vertex_count):
        angle = (2 * math.pi / vertex_count) * vertex_index
        x = center_x + int(layout_radius * math.cos(angle))
        y = center_y + int(layout_radius * math.sin(angle))
        vertex_positions.append((x, y))

    for source, destination, weight in graph:
        start = vertex_positions[source]
        end = vertex_positions[destination]
        pg.draw.line(surface, (170, 170, 170), start, end, 2)


    for source, destination, weight in mst:
        pg.draw.line(surface, (255, 0, 0), vertex_positions[source], vertex_positions[destination], 4)

    for source, destination, weight in graph:
        start = vertex_positions[source]
        end = vertex_positions[destination]
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = math.hypot(dx, dy)
        nx, ny = dx / length, dy / length

        center = (vertex_positions[source][0]+nx*circle_radius*2,vertex_positions[source][1]+ny*circle_radius*2)

        label_surface = font.render(str(weight), True, (0, 0, 0))
        label_rect = label_surface.get_rect(center=center)
        surface.blit(label_surface, label_rect)

    for vertex_index, (x, y) in enumerate(vertex_positions):
        pg.draw.circle(surface, (0, 0, 0), (x, y), circle_radius)
        pg.draw.circle(surface, (255, 255, 255), (x, y), 15)
        label_surface = font.render(str(vertex_index), True, (0, 0, 0))
        label_rect = label_surface.get_rect(center=(x, y))
        surface.blit(label_surface, label_rect)


def visual_kruskal_test():
    import time
    pg.init()
    window = pg.display.set_mode((800, 600))
    pg.display.set_caption("Kruskal MST visualization")

    edges: Graph = [
        (0, 1, 3),
        (1, 3, 15),
        (2, 3, 4),
        (2, 0, 6),
        (0, 3, 5),
        (4, 2, 4),
        (5,1,4),
        (3,5,10),
        (6,2,4),
        (7,3,5),
        (7,6,2),
        (8,1,3),
        (8,4,7),
        (9,8,1)
    ]

    vertex_count = 10
    sorted_edges = sorted(edges, key=lambda e: e[2])

    dsu = DisjointSetUnion(vertex_count)
    mst_edges: Graph = []
    current_cost = 0

    running = True
    edge_index = 0

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        if edge_index < len(sorted_edges) and len(mst_edges) < vertex_count - 1:
            edge = sorted_edges[edge_index]
            current_cost, added = process_single_edge(edge, dsu, mst_edges, current_cost)
            edge_index += 1

            window.fill((240, 240, 240))
            drawGraphWithMST(edges, mst_edges, vertex_count, window)
            pg.display.flip()

            time.sleep(1.0)  # pause so you can see each step

        else:
            window.fill((240, 240, 240))
            drawGraphWithMST(edges, mst_edges, vertex_count, window)
            pg.display.flip()

        pg.time.delay(30)

    pg.quit()


if __name__ == "__main__":
    visual_kruskal_test()