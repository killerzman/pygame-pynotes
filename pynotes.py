import pygame
import copy

class Button:
	def __init__(self, buttonImage, buttonRect):
		self.image = buttonImage
		self.rect = buttonRect

	def reset(self, buttonImage, buttonRect):
		self.__init__(buttonImage, buttonRect)

class Image:
	def __init__(self, imagePath, imageScaleWidth = 1, imageScaleHeight = 1):
		self.path = imagePath
		self.scaleW = imageScaleWidth
		self.scaleH = imageScaleHeight
		self.setup()

	def setup(self):
		self.image = pygame.image.load(self.path)
		self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*self.scaleW), int(self.image.get_height()*self.scaleH)))
		self.set_rect(0, 0)

	def reset(self, imagePath, imageScaleWidth = 1, imageScaleHeight = 1):
		self.__init__(imagePath, imageScaleWidth, imageScaleHeight)

	def set_rect(self, imageX = 0, imageY = 0):
		self.rect = pygame.Rect(imageX, imageY, self.image.get_width(), self.image.get_height())

	def set_scale(self, imageScaleWidth = 1, imageScaleHeight = 1):
		self.scaleW = imageScaleWidth
		self.scaleH = imageScaleHeight
		self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*self.scaleW), int(self.image.get_height()*self.scaleH)))

class Window:
	def __init__(self, windowWidth = 1280, windowHeight = 720, windowName = "pynotes", windowResizable = True, windowBackgroundColor = (0,0,0)):
		self.width = windowWidth
		self.height = windowHeight
		self.name = windowName
		self.resizable = windowResizable
		self.backgroundColor = windowBackgroundColor
		self.setup()

	def setup(self):
		pygame.display.set_caption(self.name)
		if self.resizable:
			self.display = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
		else:
			self.display = pygame.display.set_mode((self.width, self.height))
		self.fill(self.backgroundColor)

	def reset(self, windowWidth = 1280, windowHeight = 720, windowName = "pynotes", windowResizable = True, windowBackgroundColor = (0,0,0)):
		self.__init__(windowWidth, windowHeight, windowName, windowResizable, windowBackgroundColor)

	def fill(self, windowBackgroundColor = (0,0,0)):
		self.backgroundColor = windowBackgroundColor
		self.display.fill(self.backgroundColor)

	def draw(self, drawable, drawableX, drawableY):
		self.display.blit(drawable, (drawableX, drawableY))

	def draw_image(self, image):
		self.display.blit(image.image, (image.rect.left, image.rect.top))

def init():
	try:
		pygame.init()
		return True
	except:
		return False

def update():
	pygame.display.flip()

def main():
	running = init()
	if running:
		window = Window()
		images = {"note":Image("postitnote.png",1/6,1/6), "add":Image("plusbutton.png",1/2,1/2), "remove":Image("minusbutton.png",1/5,1/5)}

		note_rows = 5
		note_columns = 7
		note_current = 24

		note_images = []

		for i in range(note_current):
			note_images.append(Image("postitnote.png",1/6,1/6))

		for i in range(note_rows):
			for j in range(note_columns):
				note_index = i * note_columns + j
				if note_current > note_index:
					note_images[note_index].set_rect(j * note_images[note_index].image.get_width(), i * note_images[note_index].image.get_height())
					window.draw_image(note_images[note_index])

		images["add"].set_rect(0, window.height - images["add"].image.get_height())
		window.draw_image(images["add"])

		images["remove"].set_rect(images["add"].image.get_width(), window.height - images["remove"].image.get_height())
		window.draw_image(images["remove"])

		update()

		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					if images["add"].rect.collidepoint(event.pos):
						print("add")
					elif images["remove"].rect.collidepoint(event.pos):
						print("remove")
					else:
						for image_index in range(len(note_images)):
							if note_images[image_index].rect.collidepoint(event.pos):
								print(image_index + 1)
	else:
		print("pygame init failed!")

if __name__ == "__main__":
	main()