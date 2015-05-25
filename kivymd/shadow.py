# -*- coding: utf-8 -*-
from time import sleep
from threading import Thread

from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import BoundedNumericProperty, BooleanProperty, ObjectProperty
from kivy.animation import Animation

from kivymd.layouts import MaterialFloatLayout


class Shadow(ButtonBehavior, MaterialFloatLayout):
	start_visible = BooleanProperty(True)

	opacity = BoundedNumericProperty(1.0, min=0.0, max=1.0)

	_attached_to = ObjectProperty(None)
	def __init__(self, **kwargs):
		super(Shadow, self).__init__(**kwargs)
		self.register_event_type('on_visible')
		self.register_event_type('on_invisible')
		self.background_color = (0, 0, 0, self.opacity)
		self.bind(opacity=self.setter('a'))

	def _update_bg_rectangle_size(self, instance, size):
		self._bg_rect.size = size

	def fade_out(self, duration):
		if duration == 0:
			self.a = 0
			return
		anim = Animation(a=0, duration=duration, t='out_quad')
		anim.bind(on_complete=lambda *x: self.dispatch('on_invisible'))
		anim.start(self)

	def fade_in(self, duration, add_to=None):
		if duration == 0:
			self.a = self.opacity
			return
		if add_to:
			add_to.add_widget(self)
			self._attached_to = add_to
		anim = Animation(a=self.opacity, duration=duration, t='out_quad')
		anim.bind(on_complete=lambda *x: self.dispatch('on_visible'))
		anim.start(self)

	def on_visible(self):
		pass

	def on_invisible(self):
		if self._attached_to:
			self._attached_to.remove_widget(self)
