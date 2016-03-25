# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, "..")
import unittest
import overlay_handler


class TestOverlay(unittest.TestCase):

	def setUp(self):
		self.test_obj = overlay_handler.create_overlay()
		self.overlay_element = (
				overlay_handler.overlay_element_base_class("test", (0, 0)))
		self.overlay_element2 = (
					overlay_handler.overlay_element_base_class("test2", (0, 0)))
		self.test_obj.add_overlay_element(self.overlay_element)
		self.test_obj.add_overlay_element(self.overlay_element2)

	def test_alignment(self):
		self.assertEqual(self.overlay_element.pos.topleft, (0, 0))

	def test_elems(self):
		self.assertTrue(hasattr(self.test_obj, "objects"))
		self.assertIn("test", self.test_obj.objects)
		self.assertIsInstance(self.test_obj.objects["test"],
				overlay_handler.overlay_element_base_class)

	def test_generic(self):
		self.assertEqual(len(self.test_obj.objects), 2)
		self.test_obj.activate()
		for object_name in self.test_obj.objects:
			self.assertTrue(self.test_obj.objects[object_name].active)
		self.test_obj.hide()
		for object_name in self.test_obj.objects:
			self.assertFalse(self.test_obj.objects[object_name].active)

if __name__ == '__main__':
	unittest.main()
