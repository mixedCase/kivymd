# -*- coding: utf-8 -*-
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.graphics import Color, Rectangle

class BackgroundColorCapableWidget(Widget):
	r = NumericProperty(1)
	g = NumericProperty(1)
	b = NumericProperty(1)
	a = NumericProperty(0)
	background_color = ReferenceListProperty(r, g, b, a)

	def __init__(self, **kwargs):
		super(BackgroundColorCapableWidget, self).__init__(**kwargs)
		with self.canvas:
			self._bg_color = Color(rgba=(self.r, self.g, self.b, self.a))
			self._bg_rect = Rectangle(pos=(0,0))
			self.bind(size=self._update_bg_rectangle_size)
			self.bind(pos=self._update_bg_rectangle_pos)

	def _update_bg_rectangle_size(self, instance, size):
		self._bg_rect.size = size

	def _update_bg_rectangle_pos(self, instance, pos):
		self._bg_rect.pos = pos

	def on_background_color(self, instance, color):
		self._bg_color.rgba = color


class MaterialGridLayout(GridLayout, BackgroundColorCapableWidget):
	pass


class MaterialBoxLayout(BoxLayout, BackgroundColorCapableWidget):
	pass


class MaterialAnchorLayout(AnchorLayout, BackgroundColorCapableWidget):
	pass


class MaterialFloatLayout(FloatLayout, BackgroundColorCapableWidget):
	pass


class MaterialRelativeLayout(RelativeLayout, BackgroundColorCapableWidget):

	def __init__(self, **kwargs):
		super(MaterialRelativeLayout, self).__init__(**kwargs)
		self.unbind(pos=self._update_bg_rectangle_pos)
