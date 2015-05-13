# -*- coding: utf-8 -*-
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.properties import ReferenceListProperty, BooleanProperty, BoundedNumericProperty
from kivy.graphics import Color, Rectangle

class BackgroundColorCapableWidget(Widget):
	r = BoundedNumericProperty(1., min=0., max=1.)
	g = BoundedNumericProperty(1., min=0., max=1.)
	b = BoundedNumericProperty(1., min=0., max=1.)
	a = BoundedNumericProperty(0., min=0., max=1.)
	a = BoundedNumericProperty(0., min=0., max=1.)
	background_color = ReferenceListProperty(r, g, b, a)

	has_background = BooleanProperty(False)

	def __init__(self, **kwargs):
		super(BackgroundColorCapableWidget, self).__init__(**kwargs)
		with self.canvas:
			self._bg_color = Color(rgba=(self.r, self.g, self.b, self.a))
			self._bg_rect = Rectangle(pos=(0,0))
			self.bind(size=self._update_bg_rectangle_size,
					  pos=self._update_bg_rectangle_pos)

	def _update_bg_rectangle_size(self, *args):
		self._bg_rect.size = self.size

	def _update_bg_rectangle_pos(self, *args):
		self._bg_rect.pos = self.pos

	def on_background_color(self, instance, color):
		self.has_background = True if color[3] > 0 else False
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
