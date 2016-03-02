# -*- coding: utf-8 -*-
import pygame
from pygame.locals import QUIT, USEREVENT, KEYDOWN


def get_max_size(file_obj):
	from . import settings
	screen_size = (settings.screenx_current, settings.screeny_current)
	lines = file_obj.readlines()
	for test_size in range(300):
		test_size += 0
		for line in lines:
			text_img_size = modrender(line, test_size, screen_size,
										settings.color, settings.typeface)[1]
			if (text_img_size.right > settings.screenx_current
				or text_img_size.bottom > settings.screeny_current):
				return test_size - 2


def modrender(line, biggest_size, screen_size, color, typeface):
	if len(line) != 1:
		line = line[:-1]  # cut off new line
	else:
		line = " "
	is_title = (line[-1] == ":")
	has_defined_center = (":" in line[:-1])

	if is_title:
		if has_defined_center:
			tmp_font = pygame.font.SysFont(typeface, biggest_size)
			img_line = tmp_font.render(line, True, color)
			img_pos = img_line.get_rect()
			return (img_line, img_pos)
		else:
			tmp_font = pygame.font.SysFont(typeface, biggest_size)
			img_line = tmp_font.render(line, True, color)
			img_pos = img_line.get_rect()
			img_pos.centerx = screen_size[0] / 2
			return (img_line, img_pos)
	else:  # is no title
		if has_defined_center:
			tmp_font = pygame.font.SysFont(typeface, int(biggest_size * 0.8))
			img_line = tmp_font.render(line, True, color)
			left_img = tmp_font.render(line[:line.find(":")], True, color)
			center = left_img.get_rect().right
			img_pos = img_line.get_rect()
			img_pos.left = (screen_size[0] / 2) - center
			return (img_line, img_pos)
		else:
			tmp_font = pygame.font.SysFont(typeface, int(biggest_size * 0.8))
			img_line = tmp_font.render(line, True, color)
			img_pos = img_line.get_rect()
			img_pos.centerx = screen_size[0] / 2
			return (img_line, img_pos)


def run():
	"""Displays the credits"""
	from . import settings

	global lines
	global font
	global color

	color = settings.color
	typeface = settings.typeface
	lines = []
	lines_pos = []
	fade = pygame.Surface((settings.screenx_current, settings.screeny_current))
	fade.fill((0, 0, 0))
	fade.set_alpha(0)
	fade_pos = fade.get_rect()
	pygame.mouse.set_visible(False)

	fade.set_alpha(255)
	screen = settings.screen
	screen_size = (settings.screenx_current, settings.screeny_current)
	screen.blit(fade, fade_pos)
	pygame.display.flip()

	settings.upd("screenvalues")

	# load the credits.txt and assign place
	with open("./assets/lang/credits.txt") as credits_file:
		max_size = get_max_size(credits_file)
	with open("./assets/lang/credits.txt") as credits_file:
		for line in credits_file:
			line_img, line_pos = modrender(line, max_size, screen_size, color, typeface)
			lines.append(line_img)
			line_pos.y = len(lines) * max_size * 2 + settings.screeny_current + 20
			lines_pos.append(line_pos)

	# diplays content of credits.txt
	while not lines_pos[-1].top <= -80:
		settings.upd("get_events")
		for event in settings.events:
			if event.type == QUIT:
				settings.quit()

			if event.type == KEYDOWN:
				if pygame.key.name(event.key) == "escape":
					lines_pos[-1].top = -90

			if event.type == USEREVENT + 1:
				screen.blit(fade, fade_pos)
				for credit in range(len(lines)):
					screen.blit(lines[credit], lines_pos[credit])
				pygame.display.flip()
				for credit in range(len(lines)):
					lines_pos[credit].top -= 1

	pygame.mouse.set_visible(True)
