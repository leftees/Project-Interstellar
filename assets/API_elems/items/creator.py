# -*- coding: utf-8 -*-
import os
import json
from builtins import input

print(("Welcome to the Item creator setup!"))
print((""))
print(("Please enter following data to create a new Item:"))

entered_correct_data = False
while not entered_correct_data:
	name = input("\nName of the Item: ")

	if name == "":
		exit()
	elif os.path.isdir("./" + name):
		print(("\nAn item with the same name already exists."))
		print(("Please enter a new name or leave line blank if you want to abort."))
	else:
		os.mkdir("./" + name)
		entered_correct_data = True

path = os.path.abspath("./") + "/" + name + "/"

print(("\nPlease copy now the required images in the newly created folder."))
input("Press enter to run a check if every file is present.")

image_path = path + "images/"

test_finished = False
while not test_finished:
	all_files_present = (
			os.path.isdir(image_path) and
			os.path.isfile(image_path + "icon.png"))

	if not all_files_present:
		print(("\nNot all needed images are present."))
		print(("Please check again, that all images are present."))
		retry = input("Type \"retry\" to test again.\nLeave line empty to abort:")
		if not retry in ["retry", "\"retry\""]:
			exit()
	else:
		test_finished = True


dataset = {"name": name,
	"icon": image_path + "icon.png"}

datafile = open(path + "data.json", "w+")

json.dump(dataset, datafile, indent=12)
