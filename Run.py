# -*- coding: utf-8 -*-
"""
Used to start the Game and ensure that everythings works fine.
Otherwise it reports an errormessage.
"""

try:
	import pygame
	import sys
	import traceback
	import os
	try:
		import telegram
	except:
		print("Telegram not installed. No support for errors!")
	#TODO: deliver with api preinstalled
	#from libs.telegram import telegram

	import READ_BEFORE_START
	permission = READ_BEFORE_START.allow_data_collection
	if permission not in [1, -1]:
		print(("Please read the READ_BEFORE_START"))
		exit()
	if permission == 1:
		pass
	if permission == -1:
		print(("Error handling disabled :("))

	os.environ['SDL_VIDEO_CENTERED'] = '1'

	pygame.init()
	# checks if font module is availible
	pygame.font
	# Checks for correct version
	if pygame.version.ver < "1.9.1":
		raise SystemExit("Old Pygame version: " + pygame.version.ver)
	version = sys.version.split(" ")[0].split(".")
	required = "2.7.6".split(".")
	for index in range(len(required)):
		if int(required[index]) < int(version[index]):
			break
		if int(required[index]) > int(version[index]):
			raise SystemExit("Outdated Python version: " + ".".join(version))
	if sys.version[:1] >= "3":
		raise SystemExit("No support for Python3")

	# Run the game
	from src import main
	main.void()

except:
	import data as get_data
	info = sys.exc_info()
	error_type = info[1].__class__.__name__
	trace = traceback.format_exc(info[2])
	info_text = ("An error occured at client! \nTrace:\n%s\nError_Type:\n%s"
					% (trace, error_type))
	bot = telegram.Bot(token=get_data.token)
	bot.sendMessage(chat_id=158887423, text=info_text)

## Handeling errors
#except ImportError as message:
	#if str(message)[len(str(message)) - 6:] == "pygame":  # pygame not installed
		#raise SystemExit("Pygame not installed")
	#else:
		## unknown import error
		#print (("ERROR IMPORTING MODULES: %s" % message))
		#raise SystemExit(traceback.format_exc())
#except AttributeError as detail:
	## excuted if font module is not installed
	#detail = str(detail)
	#print(detail)
	#if detail[len(detail) - 5:][:4] == "font":  # Basicly the name of the module
		#raise SystemExit("Font module not installed (SDL_ttf)!")
	#else:
		#print(("Unexpected error:", sys.exc_info()[0]))
		#print("")
		#raise SystemExit(traceback.format_exc())
#except Exception as detail:
	## general errors
	#print(("Unexpected error:", sys.exc_info()[0]))
	#print("")
	#raise SystemExit(traceback.format_exc())
#