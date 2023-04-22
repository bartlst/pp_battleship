import pygame
import json
import sys
import gui

#importing config file
file = open('config.json')
config = json.load(file)

def main_menu():

    screen = pygame.display.set_mode((config['SCREEN_WIDTH'], config['SCREEN_HEIGHT']))
    pygame.display.set_caption('Battleship demo')

    #text imput
    pygame.font.init()
    base_font = pygame.font.Font(None,32)
    user_text = ''

    # create button instances
    PLAY_BUTTON = gui.Button((50, screen.get_height()/5), screen.get_width()-100, 70, '#48a302', 'PLAY')
    SETTINGS_BUTTON = gui.Button((50, screen.get_height() / 2.3), screen.get_width() - 100, 70, '#48a302', 'SETTINGS')
    QUIT_BUTTON = gui.Button((50, screen.get_height()/1.5), screen.get_width()-100, 70, '#48a302', 'QUIT')
    imput_rect = pygame.Rect(50, screen.get_height()/2.5, screen.get_width()-100, 40)
    # game loop
    menu = True
    while menu:
        screen.fill((202, 228, 241))
        #pygame.draw.rect(screen,'white',imput_rect,3)
        PLAY_BUTTON.draw(screen)
        SETTINGS_BUTTON.draw(screen)
        QUIT_BUTTON.draw(screen)

        #text_surface = base_font.render(user_text, True, (255, 255, 255))
        #screen.blit(text_surface, (imput_rect.x +5,imput_rect.y+5))
        if QUIT_BUTTON.detection():
            print('QUIT')
            pygame.quit()
            sys.exit()
        if PLAY_BUTTON.detection():
            print('PLAY')
            play_menu()

        if SETTINGS_BUTTON.detection():
            print('SETTINGS')

        # event handler
        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
#            if event.type == pygame.KEYDOWN:
#                print(text_surface.get_width())
#                print(imput_rect.width)
#                if event.key == pygame.K_BACKSPACE:
#                    user_text = user_text[:-1]
#                else:
#                    user_text += event.unicode

        pygame.display.update()



def play_menu():
    screen = pygame.display.set_mode((config['SCREEN_WIDTH'], config['SCREEN_HEIGHT']))
    play_menu_state = True
    CONNECT_BUTTON = gui.Button((50, screen.get_height() / 2.3), screen.get_width() - 100, 70, '#48a302', 'CONNECT')
    BACK_BUTTON = gui.Button((50, screen.get_height()/1.5), screen.get_width()-100, 70, '#48a302', 'BACK')
    IP_input_box = gui.InputBox(0,0,1,40)
    while play_menu_state:
        screen.fill((255, 000, 000))

        CONNECT_BUTTON.draw(screen)
        BACK_BUTTON.draw(screen)
        IP_input_box.update()
        IP_input_box.draw(screen)
        if CONNECT_BUTTON.detection():
            print('PLAY')
        if BACK_BUTTON.detection():
            print('BACK')
            play_menu_state = False
        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            IP_input_box.handle_event(event)
        pygame.display.update()

main_menu()
