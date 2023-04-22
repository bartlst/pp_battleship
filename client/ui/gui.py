import pygame
#Przeniesienie takich zmiennych jak font lub kolor do innego pliku ( daje to możliwość wprowadzenie motywu ciemnego)


#button class
class Button():

	def __init__(self, pos, width, height, color, text):
		#button surface
		self.color = color
		self.temp_color = color
		self.rect = pygame.rect.Rect(pos, (width, height))

		#text
		pygame.font.init()
		gui_font = pygame.font.Font(None,30)
		self.text_surf = gui_font.render(text,True,'#FFFFFF')
		self.text_rect = self.text_surf.get_rect(center = self.rect.center)

	def draw(self, surface):
		pygame.draw.rect(surface, self.color, self.rect)
		surface.blit(self.text_surf, self.text_rect)

	def detection(self):
		action = False
		# get mouse position
		mouse_pos = pygame.mouse.get_pos()

		# check mouseover and clicked conditions
		if self.rect.collidepoint(mouse_pos):
			#set new color when mouseover
			self.color='#66e802'
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
		else:
			self.color = self.temp_color
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		return action


class InputBox:
    def __init__(self, x, y, width, height, text='', max_len=10):
        pygame.init()
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.active = False
        self.max_len = max_len

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < self.max_len and event.unicode.isprintable():
                    self.text += event.unicode

    def update(self):
        width = max(200, self.rect.width + 10)
        self.rect.w = width

    def draw(self, screen):
        txt_surface = self.font.render(self.text, True, self.color)
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)