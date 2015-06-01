# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BoundedNumericProperty, BooleanProperty, ObjectProperty, NumericProperty
from kivy.animation import Animation

from kivymd.layouts import MaterialFloatLayout

shadow_kv = '''
<Shadow>:
	canvas:
		Color:
			rgba: 0, 0, 0, self._a
		Rectangle:
			size: self.size
			pos: self.pos

'''
class Shadow(ButtonBehavior, FloatLayout):
	start_visible = BooleanProperty(False)

	opacity = BoundedNumericProperty(1.0, min=0.0, max=1.0)

	_a = NumericProperty(0.0)
	_attached_to = ObjectProperty(None)
	def __init__(self, **kwargs):
		Builder.load_string(shadow_kv)
		super(Shadow, self).__init__(**kwargs)
		self.register_event_type('on_visible')
		self.register_event_type('on_invisible')

	def fade_out(self, duration):
		if duration == 0:
			self._a = 0.
			return
		anim = Animation(_a=0., duration=duration, t='out_quad')
		anim.bind(on_complete=lambda *x: self.dispatch('on_invisible'))
		anim.start(self)

	def fade_in(self, duration, add_to=None):
		if duration == 0:
			self.a = self.opacity
			return
		if add_to:
			add_to.add_widget(self)
			self._attached_to = add_to
		anim = Animation(_a=self.opacity, duration=duration, t='out_quad')
		anim.bind(on_complete=lambda *x: self.dispatch('on_visible'))
		anim.start(self)

	def on_visible(self):
		pass

	def on_invisible(self):
		if self._attached_to:
			self._attached_to.remove_widget(self)
