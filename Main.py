import pygame
import json
import WindowPartitioner as UI
import Fil_input as flipper
from kruskal import *
from visualizer import *
from typing import Optional, Tuple

data: Optional[Tuple[Graph, int]] = None
state = 'menu'  # 'menu' or 'visualizing'
visualization_step = 0
last_step_time = 0
step_delay = 1000  # milliseconds
dsu = None
mst_edges = []
current_cost = 0
sorted_edges = []

def quit():
    global game
    game.running = False

def toggle_overlay():
    global game
    game.esc_menu = not game.esc_menu

def toggle_menu():
    global game
    game.toggle_menu()

def main_menu():
    global game
    game.switch_menu(0)
    game.esc_menu = False
    global state
    state = 'menu'

def about():
    global game
    game.switch_menu(1)

def secret():
    global game
    game.switch_menu(2)

def input_file():
    global data, state, dsu, mst_edges, current_cost, sorted_edges
    data = flipper.skid()
    if data:
        edges, vertex_count = data
        sorted_edges = sorted(edges, key=lambda e: e[2])
        dsu = DisjointSetUnion(vertex_count)
        mst_edges = []
        current_cost = 0
        state = 'visualizing'
        game.esc_menu = False
        reset_visualization()

def reset_visualization():
    global visualization_step, last_step_time
    visualization_step = 0
    last_step_time = pygame.time.get_ticks()

def back_to_menu():
    global state
    state = 'menu'

Los_functionos_mappos = {
    "quit": quit,
    "toggle_esc_menu": toggle_overlay,
    "toggle_menu": toggle_menu,
    "main_menu" : main_menu,
    "about" : about,
    "secret" : secret,
    "input_file": input_file,
    "back_to_menu": back_to_menu
}

game = UI.Game(Los_functionos_mappos)

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((1600, 800))
    clock = pygame.time.Clock()

    game.load_menus("menu.json")

    while game.running:
        dt = clock.tick(60)  # 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state == 'menu':
                        game.switch_esc_menu(0)
                        game.esc_menu = not game.esc_menu
                    else:
                        game.switch_esc_menu(1)
                        game.esc_menu = not game.esc_menu
            if game.esc_menu:
                game.esc_event_handling(event)
                game.esc_update()
                game.esc_draw(screen)
            else:
                if state == 'menu':
                    game.menu_event_handling(event)

        if state == 'menu' and game.esc_menu != True:
            screen.fill((30, 144, 255))  # Dodger blue
            game.update()
            game.draw(screen)
        elif state == 'visualizing':
            if game.esc_menu:
                game.esc_update()
                game.esc_draw(screen)
            else:
                if data and dsu:
                    current_time = pygame.time.get_ticks()
                    if current_time - last_step_time > step_delay and visualization_step < len(sorted_edges) and len(mst_edges) < data[1] - 1:
                        edge = sorted_edges[visualization_step]
                        current_cost, added = process_single_edge(edge, dsu, mst_edges, current_cost)
                        visualization_step += 1
                        last_step_time = current_time

                    screen.fill((30, 144, 255))
                    drawGraphWithMST(data[0], mst_edges, data[1], screen)

        pygame.display.flip()

    pygame.quit()
