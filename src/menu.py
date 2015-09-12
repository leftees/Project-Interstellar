# -*- coding: utf-8 -*-
from . import settings
from . import namings
from . import objects
from . import sounds
from . import missions
from libs.pyganim import pyganim
import pygame
from libs import menu
from pygame.locals import *

"""Responsible tor the menus"""


class fade_screen():

	def __init__(self, step, step2, max_alpha, screenx, screeny):
		self.fade = pygame.Surface((screenx, screeny))
		self.fade.fill((0, 0, 0))
		self.fade.set_alpha(0)
		self.timer = pygame.time.get_ticks()
		self.alpha = 0
		self.max_alpha = max_alpha
		self.step = step
		self.step2 = step2

	def blit(self, screen):
		time = pygame.time.get_ticks()
		if (time - self.timer) > self.step and self.alpha <= self.max_alpha:
			self.timer = pygame.time.get_ticks()
			self.alpha += self.step2
		self.fade.set_alpha(self.alpha)
		screen.blit(self.fade, pygame.Rect(0, 0, 0, 0))

	def update(self, screenx, screeny):
		self.__init__(self.step, self.max_alpha, screenx, screeny)


class menu_template():

	def __init__(self, menu_name, fade_step, fade_step2, fade_max,
			variables, externals):
		"""main menu"""

		#import variables
		self.screenx = settings.screenx_current
		self.screeny = settings.screeny_current
		self.screen = settings.screen
		self.fade_step = fade_step
		self.fade_max = fade_max
		self.variables = variables
		self.externals = externals
		self.menu_name = menu_name
		self.fade_step2 = fade_step2

		#set mouse visible
		pygame.mouse.set_visible(True)

		#create menu
		self.menu = menu.create_menu(
					"./assets/templates/" + self.menu_name + ".menu",
					self.variables, pygame.Rect((0, 0), (self.screenx, self.screeny)))

		#create fade effect
		fade = fade_screen(self.fade_step, self.fade_step2, self.fade_max,
				self.screenx, self.screeny)
		self.menu.elems["externals"] = [fade]

		for elem in self.externals:
			self.menu.elems["externals"].insert(0, elem)

	class slider_post():
		"""A class for posting sliders and including their value
		as a float representative of the class. When the Class is compared
		it will compare the sliders name and reuturn the result."""
		def __init__(self, name, value):
			self.name = name
			self.value = value

		def __eq__(self, other):
			return self.name == other

		def __float__(self):
			return float(self.value)

		def __int__(self):
			return int(self.value)

		def __nonzero__(self):
			try:
				return bool(int(self.value))
			except:
				raise ValueError(
					"Could not convert {0} to bool: {1}".format(type(self.value), self.value))

		def __bool__(self):
			try:
				return bool(int(self.value))
			except:
				raise ValueError(
					"Could not convert {0} to bool: {1}".format(type(self.value), self.value))

	def run(self):

		settings.upd("get_events")
		self.menu.blit(self.screen, settings.events)
		sounds.music.update(False, False)

		events = []
		for event in settings.events:
			if event.type == QUIT:
				pygame.mouse.set_visible(False)
				events.append("event.EXIT")
			if event.type == KEYDOWN:
				key = pygame.key.name(event.key)
				if key == "escape":
					pygame.mouse.set_visible(False)
					events.append("event.QUIT")
				if key == "return":
					pygame.mouse.set_visible(False)
					events.append("event.CONTINUE")
			if event.type == USEREVENT and event.code == "MENU":
				klicked = self.menu.get_klicked()
				for elem in klicked:
					elem.klicked = False
					events.append(elem.name)
		for slider in self.menu.elems["sliders"]:
			if slider.dragged:
				if slider.is_defined_list:
					tmp_value = slider.state
				else:
					tmp_value = slider.value
				tmp_event = self.slider_post(slider.name, tmp_value)
				events.append(tmp_event)
		return(events)

	def update(self):
		for external in self.externals:
			external.update(settings.screenx_current, settings.screeny_current)
		self.__init__(self.menu_name, self.fade_step, self.fade_step2, self.fade_max,
				self.variables, self.externals)


def main():
	"""main menu"""

	#create the planets animation
	class create_planet():

		def __init__(self, screenx, screeny):
			planets = []
			src = "./assets/sprites/spinning_planet/planet-"
			for num in range(150):
				planets.append((src + str(num) + ".png", 0.065))
			planet = pyganim.PygAnimation(planets)
			planet.rotate(20)
			planet.scale((int(0.2 * screenx), int(0.2 * screenx)))
			planet_pos = planet.getRect()
			self.planet_pos = planet_pos.move(int(screenx * 0.7), int(screeny * 0.4))
			planet.play()
			self.planet = planet

		def blit(self, screen):
			self.planet.blit(screen, self.planet_pos)

		def update(self, screenx, screeny):
			self.__init__(screenx, screeny)
	planet = create_planet(settings.screenx_current, settings.screeny_current)

	#Load menu
	main_menu = menu_template("main", 70, 1, 100, {}, [planet])

	#inserts menu music
	sounds.music.queue("$not$menue.ogg", 0)
	sounds.music.play("stop")
	sounds.music.play("play", -1)

	#Define loading time on first call
	if settings.loading_time == 0:
		settings.loading_time = pygame.time.get_ticks()
	run = True

	#Menu loop
	while run:

		#Calling events and checking through events
		events = main_menu.run()
		for event in events:
			if event == "event.CONTINUE":
				run = False
			if event == "Start":
				settings.reset()
				sounds.music.play("next")
				run = False
			if event == "Settings":
				options()
				main_menu.update()
			if event == "Credits":
				namings.run()
			if event in ["Exit", "event.EXIT", "event.QUIT"]:
				settings.quit()
		pygame.display.flip()
	sounds.music.play("next", 0)


def pause():
	"""pausing menu"""

	sounds.music.play("pause")
	pygame.mouse.set_visible(True)

	background = settings.screen.copy()
	pause_menu = menu_template("pause", 5, 5, 150, {}, [])
	pause_menu.menu.elems["surfs"]["background"] = [background,
						pygame.Rect(0, 0, 0, 0)]

	run = True

	while run:

		missions.handle("pause")
		events = pause_menu.run()

		for event in events:
			if event in ["event.CONTINUE", "Continue"]:
				sounds.music.play("unpause")
				run = False
			if event == "Save Game":
				#FIXME: Out of position
				savename = inputpopup(settings.screenx_current,
						settings.screeny_current / 4,
						"Save Game")
				if savename != "Exit":
					settings.save(savename)
			if event == "Load Game":
				savegame = savegames()
				if savegame != "Exit":
					settings.load(savegame)
					sounds.music.play("unpause")
					run = False
			if event == "Settings":
				options()
				pause_menu.update()
			if event in ["Exit", "event.EXIT", "event.QUIT"]:
				main()
				run = False
		pygame.display.flip()


def choose_world():
	"""pausing menu"""

	sounds.music.play("pause")
	pygame.mouse.set_visible(True)

	background = settings.screen.copy()
	prewiev_images = []
	tmpfont = pygame.font.SysFont("monospace", 13)
	for tmp in range(8):
		prewiev_size = (int(settings.screenx_current / 5.0),
				int(settings.screeny_current / 5.0))
		surf = settings.localmap[str(tmp + 1)].background
		surf = pygame.transform.smoothscale(surf, prewiev_size)
		text = tmpfont.render("world" + str(tmp + 1), True, settings.color)
		tmprect = text.get_rect()
		tmprect.center = surf.get_rect().center
		surf.blit(text, tmprect)
		prewiev_images.append(surf)
	world_menu = menu_template("world", 5, 5, 150, {
				"image1": prewiev_images[0],
				"image2": prewiev_images[1],
				"image3": prewiev_images[2],
				"image4": prewiev_images[3],
				"image5": prewiev_images[4],
				"image6": prewiev_images[5],
				"image7": prewiev_images[6],
				"image8": prewiev_images[7]}, {})

	world_menu.menu.elems["surfs"]["background"] = [background,
						pygame.Rect(0, 0, 0, 0)]
	selected = -1

	run = True

	while run:
		events = world_menu.run()
		for event in events:
			if event in ["event.CONTINUE", "Warp"]:
				sounds.music.play("unpause")
				run = False
			if event in ["Return", "event.QUIT"]:
				selected = -1
				run = False
			if event in ["event.EXIT"]:
				settings.quit()
			if event[0:5] == "world":
				selected = event[5]
			pygame.time.wait(128)
		for elem in world_menu.menu.elems["buttons"]:
			if elem.name == "world" + str(selected):
				elem.state = 1
				#print elem.name
		pygame.display.flip()

	pygame.mouse.set_visible(False)
	missions.handle("pause")
	return selected


def inputpopup(x, y, header):
	"""Method for having an inputfield or selecting savegame"""
	#as said takes and input and returns a string or returns
	#savegame if header is saying so

	screen = settings.screen
	fade = settings.fade
	fade_pos = settings.fade_pos

	infield1 = objects.inputfield(x, y, 1, header, settings.color)
	screen.blit(fade, fade_pos)

	run = True

	while run:

		screen.blit(fade, fade_pos)

		if header == "Load Game":
			text = savegames()
			return text
		settings.upd("get_events")

		text = infield1.gettext()

		for event in settings.events:
			if event.type == KEYDOWN:
				if pygame.key.name(event.key) == "escape":
					return "Exit"

		infield1.blit()
		pygame.display.flip()

		if text is not None:
			run = False

	return text


def savegames():
	"""creates wall with savegames to select"""

	settings.upd("get_saves")

	saves = settings.saves
	screen = settings.screen
	screenx = settings.screenx_current
	screeny = settings.screeny_current
	color = settings.color
	fade = settings.fade
	fade_pos = settings.fade_pos

	xaxis = []
	yaxis = []
	saves_buttons = []
	run = True

	fade.set_alpha(20)

	for y in range(10):
		y += 1
		for x in range(5):
			x += 1
			xaxis.append(screenx / 6 * x)
			yaxis.append(screeny / 11 * y + 50)

	for a in range(len(saves)):
		tmp = saves[a].replace("\\", "/")
		saves_buttons.append(objects.button(xaxis[a], yaxis[a], tmp, color))

	a = 0
	while run:
		for a in range(len(saves)):
			saves_buttons[a].blit()
		settings.upd("get_events")
		for event in settings.events:
			if event.type == QUIT:
				settings.quit()
			if event.type == KEYDOWN:
				key = pygame.key.name(event.key)
				if key == "escape":
					return "Exit"
			if event.type == USEREVENT and event.code == "MENU":
				for a in range(len(saves)):
					if saves_buttons[a].klicked:
						pygame.display.flip()
						pygame.time.delay(200)
						return saves[a]

		pygame.display.flip()
		screen.blit(fade, fade_pos)

	run = True


def options():
	"""The settings menu"""

	button_size = menu.IO.read("./assets/templates/default.vars", "size")
	#a conversion method between selector
	#and actual text size
	#found by trial and error
	button_size = int(float(button_size) - 10) / 5

	settings_menu = menu_template("settings", 0, 0, 255,
			{"fullscreen": str(int(settings.fullscreen)),
			"volume": str(settings.volume),
			"button size": str(button_size)},
			[])

	sounds.music.play("pause")
	sounds.music.queue("$not$testsound.mp3", 0)
	sounds.music.play("play")

	run = True
	while run:

		events = settings_menu.run()
		for event in events:
			if event in ["event.EXIT", "event.QUIT", "Return"]:
				pygame.mixer.music.pause()
				sounds.music.play("unpause")
				run = False
			if event == "Volume":
				sounds.music.volume = float(event)
				settings.volume = float(event)
			if event == "Fullscreen":
				settings.fullscreen = bool(event)
			if event == "Button Size":
				button_size = int(event)
				#a conversion method between selector
				#and actual text size
				#found by trial and error
				menu.IO.write("./assets/templates/default.vars", "size",
						10 + (5 * button_size))

		sounds.music.update(False, False)
		pygame.display.flip()

	#explanation of the 10 + (5 * …) is written in
	#the Button Size handler in events loop
	menu.IO.write("./assets/templates/default.vars", "size",
			10 + (5 * button_size))
	menu.IO.write("./assets/templates/default.vars", "ratio", 1100)
	settings.upd("adjust_screen")