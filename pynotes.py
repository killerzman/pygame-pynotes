import json
import datetime
import os.path

import pygame
import pygame.locals

class NoteObject:

	attributes = ['number', 'text', 'timestamp']

	def __init__(self, noteNumber = "0", noteText = "", noteTimestamp = ""):
		self.number = noteNumber
		self.text = noteText
		self.timestamp = noteTimestamp
		self.data = {}

	def to_json(self):
		for attribute in NoteObject.attributes:
			self.data[attribute] = getattr(self, attribute)
		self.json = json.dumps(self.data)

	def from_json(self):
		self.data = json.loads(self.json)

	def save_to_file(self, number = None):
		if number:
			with open(str(number) + '.dat', 'w') as outfile:
				json.dump(self.json, outfile)
		else:
			with open(str(self.number) + '.dat', 'w') as outfile:
				json.dump(self.json, outfile)

	def load_from_file(self, number = None):
		if number:
			with open(str(number) + '.dat') as json_file:
				self.json = json.load(json_file)
		else:
			with open(str(self.number) + '.dat') as json_file:
				self.json = json.load(json_file)

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
					self.windowObject.draw_text(self.noteTexts[len(self.noteTexts) - 1],
						(self.noteImages[note_index].rect.width * (j+1) - self.noteTexts[len(self.noteTexts) - 1].fontSize / 2,
							self.noteImages[note_index].rect.height * (i+1) - self.noteTexts[len(self.noteTexts) - 1].fontSize / 2 ))

		self.images["add"].set_rect(0, self.windowObject.height - self.images["add"].image.get_height())
		self.windowObject.draw_image(self.images["add"])

		self.images["remove"].set_rect(self.images["add"].image.get_width(), self.windowObject.height - self.images["remove"].image.get_height())
		self.windowObject.draw_image(self.images["remove"])

	def note_interface_init(self):
		self.images = {"back":Image("backbutton.png",1/6,1/6), "save":Image("savebutton.png",1/4,1/4)}
		self.noteString = ""
		if self.args:
			self.noteIndex = self.args[0]
			if os.path.isfile(str(self.noteIndex) + '.dat'):
				noteobj = NoteObject()
				noteobj.load_from_file(self.noteIndex)
				noteobj.from_json()
				self.noteString = noteobj.data['text']
			self.args = None


	def note_interface(self):
		if self.args:
			if self.args[0].key == pygame.locals.K_BACKSPACE:
				self.noteString = self.noteString[:-1]
			elif self.args[0].key == pygame.locals.K_RETURN:
				self.noteString = self.noteString + "\n"
			else:
				self.noteString += str(self.args[0].unicode)
			self.args = None
		self.noteText = Text(self.noteString, textColorForeground = (255,255,255))
		self.windowObject.draw_text(self.noteText)

		self.images["back"].set_rect(0, self.windowObject.height - self.images["back"].image.get_height())
		self.windowObject.draw_image(self.images["back"])

		self.images["save"].set_rect(self.images["back"].image.get_width(), self.windowObject.height - self.images["save"].image.get_height())
		self.windowObject.draw_image(self.images["save"])

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

class Image:
	def __init__(self, imagePath, imageScaleWidth = 1, imageScaleHeight = 1):
		self.path = imagePath
		self.scaleW = imageScaleWidth
		self.scaleH = imageScaleHeight
		self.setup()

	def setup(self):
		self.image = pygame.image.load(self.path).convert_alpha()
		self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*self.scaleW), int(self.image.get_height()*self.scaleH)))
		self.set_rect(0, 0)

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

	def fill(self, windowBackgroundColor = (0,0,0)):
		self.backgroundColor = windowBackgroundColor
		self.display.fill(self.backgroundColor)

	def draw(self, drawable, drawableX, drawableY):
		self.display.blit(drawable, (drawableX, drawableY))

	def draw_image(self, image):
		self.display.blit(image.image, (image.rect.left, image.rect.top))

	'''https://stackoverflow.com/a/42015712'''
	def draw_text(self, text, pos = (0,0)):
		words = [word.split(' ') for word in text.string.splitlines()]
		space = text.fontObject.size(' ')[0]
		max_w, max_h = self.display.get_size()
		x, y = pos
		for line in words:
			for word in line:
				if text.colorBackground != (-1,-1,-1) and all(isinstance(color, int) and color >= 0 and color <= 255 for color in text.colorBackground):
					word_surface = text.fontObject.render(word, text.antialiasing, text.colorForeground, text.colorBackground)
				else:
					word_surface = text.fontObject.render(word, text.antialiasing, text.colorForeground)
				word_w, word_h = word_surface.get_size()
				if x + word_h >= max_h:
					x = pos[0]
					y += word_h
				self.display.blit(word_surface, (x,y))
				x += word_w + space
			x = pos[0]
			y += word_h

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
								noteInterface.init_draw(note_index+1)
								update_all()
								print("note " + str(note_index+1))
				elif Interface.current_interface == "note_interface":
					if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
						if noteInterface.images["back"].collide_point(event.pos):
							window.fill()
							mainInterface.draw()
							update_all()
							print("back")
						if noteInterface.images["save"].collide_point(event.pos):
							noteobj = NoteObject(noteInterface.noteIndex, noteInterface.noteString, str(datetime.datetime.now()))
							noteobj.to_json()
							noteobj.save_to_file()
							print("save")
					elif event.type == pygame.KEYDOWN:
						window.fill()
						noteInterface.draw(event)
						update_all()
						print(event.unicode)
	else:
		print("pygame init failed!")

if __name__ == "__main__":
	main()