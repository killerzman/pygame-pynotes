import pygame

def redraw_all():
	screen.fill((0,0,0))
	for i in range(note_rows):
		for j in range(note_columns):
			if note_current > (i)*note_columns + j:
				screen.blit(note_image, (j*note_image.get_width(), i*note_image.get_height()))
	
	screen.blit(plus_button_image, (0, display_y - plus_button_image.get_height()))
	screen.blit(minus_button_image, (plus_button_image.get_width(), display_y - minus_button_image.get_height()))
	screen.blit(one_button_image, (plus_button_image.get_width() + minus_button_image.get_width() + 5, display_y - one_button_image.get_height()))

	plus_button_image.get_rect().x = 0
	plus_button_image.get_rect().y = display_y - plus_button_image.get_height()

	pygame.display.flip()

if __name__ == "__main__":
	pygame.init()
	pygame.display.set_caption("pynotes")
	
	display_x = 1280
	display_y = 720

	screen = pygame.display.set_mode((display_x, display_y), pygame.RESIZABLE)

	running = True

	note_image = pygame.image.load("postitnote.png").convert_alpha()
	note_image_scale = 1/6
	note_image = pygame.transform.scale(note_image, (int(note_image.get_width()*note_image_scale), int(note_image.get_height()*note_image_scale)))

	plus_button_image = pygame.image.load("plusbutton.png").convert_alpha()
	plus_button_image_scale = 1/2
	plus_button_image = pygame.transform.scale(plus_button_image, (int(plus_button_image.get_width()*plus_button_image_scale), int(plus_button_image.get_height()*plus_button_image_scale)))
	plus_button_rect = pygame.Rect(0, display_y - plus_button_image.get_height(), plus_button_image.get_width(), plus_button_image.get_height())

	minus_button_image = pygame.image.load("minusbutton.png")
	minus_button_image_scale = 1/5
	minus_button_image = pygame.transform.scale(minus_button_image, (int(minus_button_image.get_width()*minus_button_image_scale), int(minus_button_image.get_height()*minus_button_image_scale)))
	minus_button_rect = pygame.Rect(plus_button_image.get_width(), display_y - minus_button_image.get_height(), minus_button_image.get_width(), minus_button_image.get_height())

	one_button_image = pygame.image.load("onebutton.png")
	one_button_image_scale = 1/5
	one_button_image = pygame.transform.scale(one_button_image, (int(one_button_image.get_width()*one_button_image_scale), int(one_button_image.get_height()*one_button_image_scale)))
	one_button_rect = pygame.Rect(plus_button_image.get_width() + minus_button_image.get_width() + 5, display_y - one_button_image.get_height(), one_button_image.get_width(), one_button_image.get_height())

	note_rows = 4
	note_columns = 6
	note_current = 1
	
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.VIDEORESIZE:
				display_x = event.w
				display_y = event.h
				screen = pygame.display.set_mode((display_x, display_y), pygame.RESIZABLE)
				redraw_all()
			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					if plus_button_rect.collidepoint(event.pos):
						note_current += 1
						redraw_all()
					if minus_button_rect.collidepoint(event.pos):
						note_current -= 1
						redraw_all()
					if one_button_rect.collidepoint(event.pos):
						note_current = 1
						redraw_all()
				'''print(screen.get_width(), screen.get_height())'''

	pygame.quit()