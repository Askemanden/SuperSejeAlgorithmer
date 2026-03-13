import pygame
import json
import WindowPartitioner as UI
import Fil_input as flipper

def quit():
    game.running = False

def toggle_overlay():
    game.esc_menu = not game.esc_menu

def toggle_menu():
    game.toggle_menu()

def input_file():
    kruskal_dict = flipper.skid()      #<--- ASKE SKID() RETURNERER EN ORDBOG, GØR NOGET MED DEN # "flipper.skid() er self-evident 📜🪶🦄"

Los_functionos_mappos = {
    "quit": quit,
    "toggle_esc_menu" : toggle_overlay,
    "toggle_menu" : toggle_menu,
    "input_file" : input_file
}

game = UI.Game(Los_functionos_mappos)


if __name__ == "__main__":
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

        #Asekslasek-kode indsættes her:

        pygame.display.flip()
    pygame.quit()
