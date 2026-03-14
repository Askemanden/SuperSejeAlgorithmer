import pygame
import json
import WindowPartitioner as UI
import Fil_input as flipper
from kruskal import*
from visualizer import *
import time

data : Tuple[Graph, int] | None= None

def quit():
    game.running = False

def toggle_overlay():
    game.esc_menu = not game.esc_menu

def toggle_menu():
    game.toggle_menu()

def input_file():
    global data
    data = flipper.skid()      #<--- ASKE SKID() RETURNERER EN ORDBOG, GØR NOGET MED DEN # "flipper.skid() er self-evident 📜🪶🦄"
    print(data)

Los_functionos_mappos = {
    "quit": quit,
    "toggle_esc_menu" : toggle_overlay,
    "toggle_menu" : toggle_menu,
    "input_file" : input_file
}

game = UI.Game(Los_functionos_mappos)


if __name__ == "__main__":

    m = 0

    Slaske = 0
    Aske = Slaske

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((1600, 800))

    game.load_menus("menu.json")

    while game.running != False:
        # Main loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game.esc_menu = not game.esc_menu
            
            if game.esc_menu != True:
                # Håndter normal menu
                game.menu_event_handling(event)
            else:
                # Håndter pausemenuen
                game.esc_event_handling(event)
                
        if game.esc_menu != False:
            #opdaterer og håndterer pausemenuen.
            game.esc_update()
            game.esc_draw(screen)
            pygame.display.flip()
            continue

        screen.fill((30, 144, 255))  # Dodger blue
        game.update()
        game.draw(screen)


        pygame.display.flip()

        print(data)
        print(m)
        m+=1
        if data != None: 
            print(2)
            edges = data[0]
            vertex_count = data[1]

            sorted_edges = sorted(edges, key=lambda e: e[2])

            dsu = DisjointSetUnion(vertex_count)
            mst_edges: Graph = []
            current_cost = 0

            running = True
            edge_index = 0

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                if edge_index < len(sorted_edges) and len(mst_edges) < vertex_count - 1:
                    edge = sorted_edges[edge_index]
                    current_cost, added = process_single_edge(edge, dsu, mst_edges, current_cost)
                    edge_index += 1

                    screen.fill((240, 240, 240))
                    drawGraphWithMST(edges, mst_edges, vertex_count, screen)
                    pygame.display.flip()

                    time.sleep(1.0)  

                else:
                    screen.fill((240, 240, 240))
                    drawGraphWithMST(edges, mst_edges, vertex_count, screen)
                    pygame.display.flip()

                pygame.time.delay(30)

                pygame.display.flip()

    pygame.quit()
