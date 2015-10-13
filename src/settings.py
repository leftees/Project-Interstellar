# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from libs.pyganim import pyganim
import os
import shutil
import sys
import traceback
import random
import json


def init():

	global up  # player should move up
	global down  # player should move down
	global left  # player should move left
	global right  # player should move right
	global konstspeed  # some konstant for speed
	global clock  # clock object of pygame
	global stdfont  # global font defenition
	global typeface  # the typeface...
	global fullscreen  # determines current state if fullscreen or not
	global fullscreenold  # used to check if fullscreen has changes
	global screen  # the screen
	global screenx  # maximum x pixels
	global screeny  # maximum y pixels
	global aspect_ratio  # aspect ratio
	global screenx_current  # current x pixels
	global screeny_current  # current y pixels
	global fake_size  # the ratio of screenx_current and size of the background
	global bullets  # list of all bullets
	global dstars  # amount of stars
	global debugscreen  # determines wether to show debug info
	global debugmode  # Enables debugmode
	global isnear  # easteregg
	global background  # background image
	global field  # image for the inputfield
	global bullet_img  # image for the bullet
	global targeton_img  # surf for target whenlight turned on
	global targetoff_img  # surf for target when turned off
	global code  # used for custom user events
	global events  # events
	global music  # the music playlist object
	global color  # global color defenition
	global skip  # unsused (currently)
	global volume  # volume
	global musics  # the list of music titles assoziated wih the music files
	global saves  # all savegames
	global psycomode  # if psycomode is turned on
	global explosions  # list of surfs of explosions
	global explosions_disp  # list of showing explosions
	global run  # boolean for main loop
	global dtargets  # amount of targets
	global morevents  # custom event logger
	global infinitevents  # A event logger which retriggers as long as condition
	global musicend  # custom event number to show that music ended
	global border1  # A box to hold the status information about energy level
	global world  # a placeholder for the world class
	global objects_on_screen  # entitys currently blitted to screen
	global player  # abstract player class
	global localmap  # A dict of the local worlds
	global loading_time  # time until first blit
	global seed  # the environments seed

	# for this operation os.urandom is used
	seed_size = 16
	seed = random.randint(10 ** (seed_size - 1), (10 ** seed_size) - 1)
	random.seed(seed)

	# set up screen
	pygame.event.set_grab(False)
	pygame.mouse.set_visible(False)

	screenx = pygame.display.Info().current_w
	screeny = pygame.display.Info().current_h
	pygame.display.set_mode((1, 1))
	aspect_ratio = screenx / float(screeny)
	screenx_current = screenx
	screeny_current = screeny

	# create empty folders if needed
	if not os.path.exists("./assets/sprites/player/"):
		os.makedirs("./assets/sprites/player/")
	if not os.path.exists("./screenshots/"):
		os.makedirs("./screenshots/")

	# load images and convert them to the fatest blittable format
	background = pygame.image.load("./assets/sprites/Background2.tif").convert()
	field = pygame.image.load("./assets/sprites/inputbox1.tif").convert_alpha()
	bullet_img = pygame.image.load("./assets/sprites/Bullet.tif").convert_alpha()
	targeton_img = pygame.image.load("./assets/sprites/mine_on.tif"
				).convert_alpha()
	targetoff_img = pygame.image.load("./assets/sprites/mine_off.tif"
				).convert_alpha()
	border1 = pygame.image.load("./assets/sprites/bar1.tif").convert_alpha()

	# define some konstants or default values
	clock = pygame.time.Clock()
	typeface = "monospace"
	stdfont = pygame.font.SysFont(typeface, 15)

	version = "0.3.3.1 dev"
	up = False
	down = False
	left = False
	right = False
	konstspeed = 0.0025
	fullscreen = False
	debugscreen = False
	debugmode = True
	dstars = 500
	isnear = "False"
	code = ""
	events = []
	color = (255, 255, 10)
	skip = False
	volume = 0.5
	fullscreenold = False
	fake_size = 8 / 7.0
	psycomode = False
	run = True
	dtargets = 5
	morevents = []
	bullets = []
	infinitevents = {"fire1": False, "roundfire": False}
	musicend = USEREVENT + 100
	events = []
	loading_time = 0

	from .player import player as player
	player = player()

	pygame.display.set_caption("Project Interstellar " + version)
	pygame.display.set_icon(pygame.image.load("./assets/sprites/logo.png"))

	# more complex default settings like creation of stars and targets and so on
	if debugmode:
		# Add custom handler here for when debugmode is activated
		volume = 0.0
		# fullscreen = False
		pass

	def get_anim_source(num, quantity):
		animationsourcetmp = []
		if num >= 10:
			num = str(num)
		else:
			num = "0" + str(num)
		for a in range(quantity):
			a = str(a)
			if int(a) < 10:
				a = "0" + str(a)
			tmp = ("./assets/sprites/explosions/expl_" + num + "_00" + a + ".tif", 0.04)
			animationsourcetmp.append(tmp)
		return animationsourcetmp

	explosion9 = pyganim.PygAnimation(get_anim_source(9, 32), loop=False)
	explosion10 = pyganim.PygAnimation(get_anim_source(10, 32), loop=False)
	explosion11 = pyganim.PygAnimation(get_anim_source(11, 24), loop=False)
	explosions = [explosion9, explosion10, explosion11]
	explosions_disp = []

	upd("get_saves")

	if fullscreen:
		screen = pygame.display.set_mode(
			(screenx_current, screeny_current),
			pygame.FULLSCREEN, 32)
	if not fullscreen:
		screenx_current = int(screenx_current / 2.0)
		screeny_current = int(screeny_current / 2.0)
		screen = pygame.display.set_mode((screenx_current, screeny_current),
		0, 32)

	from . import worlds
	localmap = {}
	for a in range(8):
		world = worlds.world(str(a + 1))
		world.generate(background, dstars, dtargets)
		localmap[str(a + 1)] = world
	world = localmap["1"]
	upd("adjust_screen")

	#scales images so they fill screen especially when not 16/9 ar
	if aspect_ratio > 16.0 / 9:
		ratio = screenx_current / float(background.get_size()[1])
		pygame.transform.smoothscale(background,
					(screenx_current, screeny_current * ratio))
	elif aspect_ratio < 16.0 / 9:
		ratio = screeny_current / float(background.get_size()[0])
		pygame.transform.smoothscale(background,
					(screenx_current * ratio, screeny_current))


def reset():

	"""resets some settings"""
	global konstspeed
	global color

	pygame.event.set_grab(False)
	pygame.mouse.set_visible(False)

	player.reset()

	konstspeed = 0.0025
	color = (255, 255, 10)

	from . import missions
	missions.handle("pause")

	if debugmode:
		fullscreen = False  # lint:ok

	world.generate(world.background, dstars, dtargets)


def upd(level):

	"""updates various variables"""
	if level == "get_events":
		global events
		events = pygame.fastevent.get()
		return
	if level == "screenvalues":
		global screenx_current
		global screeny_current
		global aspect_ratio
		screenx_current = pygame.display.Info().current_w
		screeny_current = pygame.display.Info().current_h
		aspect_ratio = screenx_current / float(screeny_current)
		return
	if level == "get_saves":
		global saves
		saves = []
		for elem in os.listdir("./saves/"):
			if os.path.isdir("./saves/" + elem):
				saves.append(elem)
		return
	if level == "adjust_screen":
		global background
		global background_pos
		global konstspeed
		#FIXME: fullscreenold is redundant
		global fullscreenold
		global fullscreen

		if fullscreen:
			pygame.display.set_mode((screenx, screeny), pygame.FULLSCREEN)
		if not fullscreen:
			pygame.display.set_mode((screenx_current, screeny_current))

		upd("screenvalues")

		konstspeed = 0.0025
		konstspeed = konstspeed * (screenx_current / 1920.0)

		world.adjust_to_screen()

		#scales images so they fill screen especially when not 16/9 ar
		if aspect_ratio > 16.0 / 9:
			ratio = screenx_current / float(background.get_size()[1])
			pygame.transform.smoothscale(background,
						(screenx_current, int(screeny_current * ratio)))
		elif aspect_ratio < 16.0 / 9:
			ratio = screeny_current / float(background.get_size()[0])
			pygame.transform.smoothscale(background,
						(int(screenx_current * ratio), screeny_current))

		return
	print("Something went wrong here")
	raise Exception


def toggle(var, option1, option2):
	# toggles between option1 and 2 and retunr var, saves some space
	if var == option1:
		var = "yep"
	if var == option2:
		var = option1
	if var == "yep":
		var = option2
	return var


class data():

	def __init__(self):
		"""create a new savegame"""
		pass

	def save(self, name):

		from . import sounds
		name = name.encode("utf-8")
		# removes invalid characters
		if "/" in name:
			name = name.replace("/", "\\")
		if "%" in name:
			name = name.replace("%", "")

		if not os.path.isdir("./saves/%s/" % name):
			os.makedirs("./saves/%s/" % name)

		all_world_data = {}
		world_image = {}
		for world_name in localmap:
			if not os.path.isdir("./saves/%s/%s" % (name, world_name)):
				os.makedirs("./saves/%s/%s" % (name, world_name))
			all_world_data[world_name] = {}
			all_world_data[world_name]["targets"] = []
			all_world_data[world_name]["station"] = {}
			for target in localmap[world_name].targets:
				savable_vars = {}
				for inst_var in target.__dict__:
					if type(target.__dict__[inst_var]) in [list, str, int, float, bool]:
						savable_vars[inst_var] = target.__dict__[inst_var]
				all_world_data[world_name]["targets"].append(savable_vars)
			savable_vars = {}
			station_vars = localmap[world_name].warp1.__dict__
			for inst_var in station_vars:
				if type(station_vars[inst_var]) in [list, str, int, float, bool]:
					savable_vars[inst_var] = station_vars[inst_var]
			all_world_data[world_name]["station"] = (savable_vars)
			world_image[world_name] = localmap[world_name].background

		data = {"fullscreen": fullscreen,
			"screenx_current": screenx_current,
			"screeny_current": screeny_current,
			"debugmode": debugmode,
			"debugscreen": debugscreen,
			"player.rel_x": player.rel_x,
			"player.rel_y": player.rel_y,
			"sounds.music.volume": sounds.music.volume,
			"player.timeplay": player.timeplay,
			"world.name": world.name,
			"worlds": list(localmap.keys())
			}

		settings_file = open("./saves/" + name + "/Data.json", "w")
		for world_name in localmap:
			world_file = open("./saves/%s/%s/world.json" % (name, world_name), "w")
			pygame.image.save(world_image[world_name],
					"./saves/%s/%s/background.tga" % (name, world_name))
			json.dump(all_world_data[world_name], world_file, indent=12)
		json.dump(data, settings_file, indent=12)

	def load(self, name):
		"""Load savegame"""
		from . import sounds
		from . import objects
		global fullscreen
		global screenx_current
		global screeny_current
		global debugmode
		global debugscreen
		global localmap
		global world
		try:
			data = json.load(open("./saves/" + unicode(name) + "/Data.json", "r"))
			fullscreen = data["fullscreen"]
			screenx_current = data["screenx_current"]
			screeny_current = data["screeny_current"]
			debugmode = data["debugmode"]
			debugscreen = data["debugscreen"]
			player.rel_x = data["player.rel_x"]
			player.rel_y = data["player.rel_y"]
			sounds.music.volume = data["sounds.music.volume"]
			player.timeplay = data["player.timeplay"]
			world_names = data["worlds"]

			from . import worlds
			localmap = {}
			for world_name in world_names:
				background_dir = "./saves/%s/%s/background.tga" % (name, world_name)
				background = pygame.image.load(background_dir)
				world_data = json.load(open("./saves/%s/%s/world.json"
							% (name, world_name), "r"))
				localmap[world_name] = worlds.world(world_name)
				localmap[world_name].generate(background, dstars, 0)
				for target_data in world_data["targets"]:
					tmp_target = objects.target()
					tmp_target.pos_xper = target_data["pos_xper"]
					tmp_target.pos_yper = target_data["pos_yper"]
					tmp_target.timer = target_data["timer"]
					tmp_target.update()
					localmap[world_name].targets.append(tmp_target)
				tmp_station = objects.warp_station()
				tmp_station.x_pos = world_data["station"]["x_pos"]
				tmp_station.y_pos = world_data["station"]["y_pos"]
				tmp_station.update()
				localmap[world_name].warp1 = tmp_station
			world = localmap[data["world.name"]]
		except Exception:
			print(("Unexpected error:", sys.exc_info()[0]))
			print((traceback.format_exc()))


def quit():
	"""Routine for exiting"""
	from . import midi_in
	midi_in.quit()
	pygame.quit()
	shutil.rmtree('./assets/sprites/player')
	sys.exit()
