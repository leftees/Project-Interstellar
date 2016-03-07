# -*- coding: utf-8 -*-
import pygame


class create_overlay():
	"""A mother-class for in-game overlays.

	init(self) inits the module
	add_overlay(self, overlay_obj) adds an overlay element"""

	def __init__(self):
		self.objects = {}
		self.objs_on_screen = set()

	def add_overlay_element(self, overlay_obj):
		"""Adds an overlay element to the whole overlay.

		This method requires an instance.
		It is called as follows: instance.add_overlay_element(overlay_obj)
		For custom objects see class overlay_object.
		"""
		self.objects[overlay_obj.name] = overlay_obj

	def enable(self, name_list):
		"""Enable the overlay."""
		tmp_list = []
		if name_list == "all":
			tmp_list = [self.objects[elem] for elem in self.objects.keys()]
		else:
			if type(name_list) == str:
				name_list = [name_list]
			for obj in self.objects:
				if obj in name_list:
					tmp_list.append(self.objects[obj])
		self.objs_on_screen.update(tmp_list)

	def disable(self, name_list):
		"""Disable the overlay."""
		if name_list == "all":
			self.objs_on_screen = set()
		else:
			if type(name_list) == str:
				name_list = name_list.split(",")
			for obj in self.objects:
				if obj in name_list:
					self.objs_on_screen.remove(self.objects[obj])
					return

	def blit(self, screen):
		for obj in self.objects:
			pass


class create_overlay_object():
	"""This is an element which can be used in an overlay"""

	def __init__(self, name):
		self.name = name
		self.img = pygame.Surface((0, 0))
		self.pos = pygame.Rect(0, 0, 0, 0)
