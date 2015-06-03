# -*- coding: utf-8 -*-
from kivy.core.window import Window


def get_device_orientation():
	if Window.width > Window.height:
		return "landscape"
	elif Window.height > Window.width:
		return "portrait"
	else:
		# Just in case some evil company makes a 1:1 screen, let our user know
		# with a None. Matter of time before we see a smartwatch like that.
		return


def bind_to_rotation(callback):
	Window.bind(size=lambda x, y: __bind_to_rotation_helper(callback))


def __bind_to_rotation_helper(callback):
	callback(get_device_orientation())