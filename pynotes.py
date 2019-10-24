import pygame
import pygame.locals

class Interface:

	current_interface = ""

	def __init__(self, windowObject, interfaceName):
		self.windowObject = windowObject
		self.interfaceName = interfaceName
		self.args = None

	def set_curr_interface(self):
		Interface.current_interface = self.interfaceName

	def init_draw(self, *args):
		if args:
			self.args = args
		getattr(Interface, self.interfaceName + "_init")(self)
		self.draw()

	def draw(self, *args):
		if args:
			self.args = args
		getattr(Interface, self.interfaceName)(self)
		self.set_curr_interface()

	def main_interface_init(self):
		self.images = {"note":Image("postitnote.png",1/6,1/6), "add":Image("plusbutton.png",1/2,1/2), "remove":Image("minusbutton.png",1/5,1/5)}

		self.noteRows = 6
		self.noteColumns = 6
		self.noteCurrent = 1

	def main_interface(self):
		self.noteTexts = []
		self.noteImages = []

		for i in range(self.noteCurrent):
			self.noteImages.append(Image("postitnote.png",1/6,1/6))

		for i in range(self.noteRows):
			for j in range(self.noteColumns):
				note_index = i * self.noteColumns + j
				if self.noteCurrent > note_index:
					self.noteImages[note_index].set_rect(j * self.noteImages[note_index].image.get_width(), i * self.noteImages[note_index].image.get_height())
					self.windowObject.draw_image(self.noteImages[note_index])
					self.noteTexts.append(Text(str(note_index + 1), textColorForeground = (255,255,255)))
					self.noteTexts[len(self.noteTexts) - 1].rect.center = (self.noteImages[note_index].rect.width * (j+1), self.noteImages[note_index].rect.height * (i+1))
					self.windowObject.draw_text(self.noteTexts[len(self.noteTexts) - 1])

		self.images["add"].set_rect(0, self.windowObject.height - self.images["add"].image.get_height())
		self.windowObject.draw_image(self.images["add"])

		self.images["remove"].set_rect(self.images["add"].image.get_width(), self.windowObject.height - self.images["remove"].image.get_height())
		self.windowObject.draw_image(self.images["remove"])

	def note_interface_init(self):
		self.images = {"back":Image("backbutton.png",1/5,1/5)}
		self.noteString = ""

	def note_interface(self):
		'''self.noteText = Text("Note number " + str(self.args[0]+1), textColorForeground = (255,255,255))
		self.noteText.rect.center = (self.windowObject.width // 2, self.windowObject.height // 2)
		self.windowObject.draw_text(self.noteText)'''

		if self.args:
			if self.args[0].key == pygame.locals.K_BACKSPACE:
				self.noteString = self.noteString[:-1]
			else:
				self.noteString += str(self.args[0].unicode)
			self.args = None
		self.noteText = Text(self.noteString, textColorForeground = (255,255,255))
		self.windowObject.draw_text(self.noteText)

		self.images["back"].set_rect(0, self.windowObject.height - self.images["back"].image.get_height())
		self.windowObject.draw_image(self.images["back"])

class Text:
	def __init__(self, textString = "default", textFontSize = 20, textFontType = 'freesansbold.ttf', textColorForeground = (0,0,0), textColorBackground = (-1,-1,-1), textAntialiasing = True):
		self.string = textString
		self.fontType = textFontType
		self.fontSize = textFontSize
		self.colorForeground = textColorForeground
		self.colorBackground = textColorBackground
		self.antialiasing = textAntialiasing
		self.setup()

	def setup(self):
		self.fontObject = pygame.font.Font(self.fontType, self.fontSize)
		if self.colorBackground != (-1,-1,-1) and all(isinstance(color, int) and color >= 0 and color <= 255 for color in self.colorBackground):
			self.textObject = self.fontObject.render(self.string, self.antialiasing, self.colorForeground, self.colorBackground)
		else:
			self.textObject = self.fontObject.render(self.string, self.antialiasing, self.colorForeground)
		self.rect = self.textObject.get_rect()

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

	def draw_text(self, text):
		self.display.blit(text.textObject, text.rect)

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
							mainInterface.noteCurrent += 1
							mainInterface.draw()
							update_all()
							print("add")
						if mainInterface.images["remove"].collide_point(event.pos):
							window.fill()
							mainInterface.noteCurrent -= 1
							mainInterface.draw()
							update_all()
							print("remove")
						for note_index in range(len(mainInterface.noteImages)):
							if mainInterface.noteImages[note_index].collide_point(event.pos):
								window.fill()
								noteInterface.init_draw()
								update_all()
								print("note " + str(note_index+1))
				elif Interface.current_interface == "note_interface":
					if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
						if noteInterface.images["back"].collide_point(event.pos):
							window.fill()
							mainInterface.draw()
							update_all()
							print("back")
					elif event.type == pygame.KEYDOWN:
						window.fill()
						noteInterface.draw(event)
						update_all()
						print(event.unicode)
	else:
		print("pygame init failed!")

if __name__ == "__main__":
	main()