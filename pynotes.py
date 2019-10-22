import pygame

class Interface:

	current_interface = ""

	def __init__(self, windowObject, interfaceName):
		self.windowObject = windowObject
		self.interfaceName = interfaceName

	def set_curr_interface(self):
		Interface.current_interface = self.interfaceName

	def init_draw(self):
		getattr(Interface, self.interfaceName + "_init")(self)
		self.draw()
		self.set_curr_interface()

	def draw(self):
		getattr(Interface, self.interfaceName)(self)
		self.set_curr_interface()

	def main_interface_init(self):
		self.images = {"note":Image("postitnote.png",1/6,1/6), "add":Image("plusbutton.png",1/2,1/2), "remove":Image("minusbutton.png",1/5,1/5)}

		self.note_rows = 5
		self.note_columns = 7
		self.note_current = 20

	def main_interface(self):
		self.note_images = []

		for i in range(self.note_current):
			self.note_images.append(Image("postitnote.png",1/6,1/6))

		for i in range(self.note_rows):
			for j in range(self.note_columns):
				note_index = i * self.note_columns + j
				if self.note_current > note_index:
					self.note_images[note_index].set_rect(j * self.note_images[note_index].image.get_width(), i * self.note_images[note_index].image.get_height())
					self.windowObject.draw_image(self.note_images[note_index])

		self.images["add"].set_rect(0, self.windowObject.height - self.images["add"].image.get_height())
		self.windowObject.draw_image(self.images["add"])

		self.images["remove"].set_rect(self.images["add"].image.get_width(), self.windowObject.height - self.images["remove"].image.get_height())
		self.windowObject.draw_image(self.images["remove"])

	def note_interface_init(self):
		font = pygame.font.Font('freesansbold.ttf', 32)
		text = font.render('dinamo', True, (255,255,255), (0,0,0))
		textRect = text.get_rect()
		textRect.center = (self.windowObject.width // 2, self.windowObject.height // 2)
		self.windowObject.display.blit(text, textRect)

	def note_interface(self):
		pass


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

	def collide_point(self, position):
		return self.rect.collidepoint(position)

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

def update_all():
	pygame.display.flip()

def main():
	running = init()
	if running:
		window = Window()

		mainInterface = Interface(window, "main_interface")
		mainInterface.init_draw()

		noteInterface = Interface(window, "note_interface")

		update_all()

		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				if Interface.current_interface == "main_interface":
					if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
						if mainInterface.images["add"].collide_point(event.pos):
							window.fill()
							mainInterface.note_current += 1
							mainInterface.draw()
							update_all()
							print("add")
						if mainInterface.images["remove"].collide_point(event.pos):
							window.fill()
							mainInterface.note_current -= 1
							mainInterface.draw()
							update_all()
							print("remove")
						for note_index in range(len(mainInterface.note_images)):
							if mainInterface.note_images[note_index].collide_point(event.pos):
								window.fill()
								noteInterface.init_draw()
								update_all()

	else:
		print("pygame init failed!")

if __name__ == "__main__":
	main()