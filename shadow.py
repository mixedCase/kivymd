# -*- coding: utf-8 -*-
from layouts import MaterialFloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import BoundedNumericProperty, BooleanProperty
from time import sleep
from threading import Thread


class Shadow(ButtonBehavior, MaterialFloatLayout):

	start_visible = BooleanProperty(True)

	opacity = BoundedNumericProperty(1.0, min=0.0, max=1.0)

	def __init__(self, **kwargs):
		super(Shadow, self).__init__(**kwargs)
		self.background_color = (0,0,0, self.opacity)
		self.bind(opacity=self.setter('a'))

	def _update_bg_rectangle_size(self, instance, size):
		self._bg_rect.size = size

	def fade_out(self, duration, fps=60, remove_from=None):
		if duration == 0:
			self.a = 0
			return
		total_steps = duration * float(fps)
		step = self.opacity/total_steps
		t = Thread(target=self._fade_out, args=(step, fps, remove_from))
		t.start()

	def _fade_out(self, step, fps, remove_from):
		while self.a > 0:
			sleep(1.0/fps)
			self.a -= step
		self.a = 0
		if remove_from:
			remove_from.remove_widget(self)

	def fade_in(self, duration, fps=60, add_to=None):
		if duration == 0:
			self.a = self.opacity
			return
		total_steps = duration * float(fps)
		step = self.opacity/total_steps
		t = Thread(target=self._fade_in, args=(step, fps, add_to))
		t.start()

	def _fade_in(self, step, fps, add_to):
		if add_to:
			add_to.add_widget(self)
		while self.a < self.opacity:
			sleep(1.0/fps)
			self.a += step
		self.a = self.opacity
