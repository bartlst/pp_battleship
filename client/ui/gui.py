import pygame
import sys

class Button:
    def __init__(self, text, width, height, pos):
        #tep rectangle
        self.top_rect = pygame.Rect(pos, (width,height))
        self.top_color = '#FF4747'

        #text
        self.text_surf = gui_font.render(text,True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect()


pygame.init()
screen = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()
gui_font = pygame.font.Font(None,30)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        screen.fill('#DCDDD8')

        pygame.display.update()
        clock.tick(60)