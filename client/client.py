import pygame
import json
import sys
from ui import gui

#importing config file
file = open('ui/config.json')
config = json.load(file)

def main_menu():

    screen = pygame.display.set_mode((config['SCREEN_WIDTH'], config['SCREEN_HEIGHT']))
    pygame.display.set_caption('Battleship demo')

    # create button instances
    PLAY_BUTTON = gui.Button((50, screen.get_height()/2), screen.get_width()-100, 70, '#48a302', 'Connect')
#    OPTIONS_BUTTON = gui.Button((100, 250), 100, 70, '#48a302', 'OPTIONS')
    QUIT_BUTTON = gui.Button((50, screen.get_height()/1.5), screen.get_width()-100, 70, '#48a302', 'QUIT')
    screen.fill((202, 228, 241))
    # game loop
    menu = True
    options_menu = False
    while menu:
        PLAY_BUTTON.draw(screen)
#        OPTIONS_BUTTON.draw(screen)
        QUIT_BUTTON.draw(screen)

        if PLAY_BUTTON.detection():
            print('PLAY')
#        if OPTIONS_BUTTON.detection():
#            print('OPTIONS')

        if QUIT_BUTTON.detection():
            pygame.quit()
            sys.exit()
        # event handler
        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

main_menu()
