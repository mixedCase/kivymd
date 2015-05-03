# -*- coding: utf-8 -*-
from kivy.metrics import dp
from layouts import MaterialRelativeLayout


class Divider(MaterialRelativeLayout):

	def __init__(self, color=(0,0,0,0.12), **kwargs):
		super(Divider, self).__init__(**kwargs)
		self.color = color
		self.size_hint_y = None
		self.height = dp(1)

	@property
	def color(self):
		return self.background_color

	@color.setter
	def color(self, value):
		self.background_color = value