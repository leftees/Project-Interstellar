# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, "..")
import unittest
import overlay_handler


class TestOverlay(unittest.TestCase):

	def setUp(self):
		self.test_obj = overlay_handler.create_overlay()
		self.overlay_element = overlay_handler.create_overlay_object("test")
		self.overlay_element2 = overlay_handler.create_overlay_object("test2")
		self.test_obj.add_overlay_element(self.overlay_element)
		self.test_obj.add_overlay_element(self.overlay_element2)

	def test_elems(self):
		self.assertTrue(hasattr(self.test_obj, "objects"))
		self.assertIn("test", self.test_obj.objects)
		self.assertIsInstance(self.test_obj.objects["test"],
								overlay_handler.create_overlay_object)

	def test_generic(self):
		self.assertEqual(len(self.test_obj.objects), 2)
		self.test_obj.enable("all")
		self.assertEqual(len(self.test_obj.objs_on_screen), 2)
		self.test_obj.disable("all")
		self.assertEqual(len(self.test_obj.objs_on_screen), 0)
		self.test_obj.enable("test")
		self.assertEqual(len(self.test_obj.objs_on_screen), 1)
		self.test_obj.disable("test")
		self.assertEqual(len(self.test_obj.objs_on_screen), 0)
		self.assertEqual(len(self.test_obj.objects), 2)

if __name__ == '__main__':
	unittest.main()
