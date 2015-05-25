# -*- coding: utf-8 -*-

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.properties import ReferenceListProperty, BooleanProperty, BoundedNumericProperty, AliasProperty
from kivy.graphics import Color, Rectangle
from material_resources import get_color_tuple, get_rgba_color

class BackgroundColorCapableWidget(Widget):
	r = BoundedNumericProperty(1., min=0., max=1.)
	g = BoundedNumericProperty(1., min=0., max=1.)
	b = BoundedNumericProperty(1., min=0., max=1.)
	a = BoundedNumericProperty(0., min=0., max=1.)
	a = BoundedNumericProperty(0., min=0., max=1.)
	background_color = ReferenceListProperty(r, g, b, a)

	def _get_bg_color_tuple(self):
		return get_color_tuple(self.background_color)

	def _set_bg_color_from_tuple(self, tuple):
		self.background_color = get_rgba_color(tuple)

	background_color_tuple = AliasProperty(_get_bg_color_tuple, _set_bg_color_from_tuple,
										   bind=('background_color', ))

	has_background = BooleanProperty(False)

	def __init__(self, **kwargs):
		super(BackgroundColorCapableWidget, self).__init__(**kwargs)
		with self.canvas:
			self._bg_color = Color(rgba=(self.r, self.g, self.b, self.a))
			self._bg_rect = Rectangle(pos=(0, 0))

		self.bind(size=self._update_bg_rectangle_size,
				  pos=self._update_bg_rectangle_pos,
				  background_color=self._set_bg_color)

	def _update_bg_rectangle_size(self, *args):
		self._bg_rect.size = self.size


	def _update_bg_rectangle_pos(self, *args):
		self._bg_rect.pos = self.pos


	def _set_bg_color(self, instance, color):
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
