# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.properties import StringProperty, NumericProperty, ListProperty, OptionProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp, sp
from layouts import MaterialFloatLayout, MaterialBoxLayout
from kivymd.label import MaterialLabel
from ripplebehavior import RippleBehavior
from elevationbehaviour import ElevationBehaviour
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

from theme import ThemeBehaviour


class MaterialIcon(ThemeBehaviour, RippleBehavior, ButtonBehavior, MaterialBoxLayout):
	"""A 48x48 icon that behaves like a button.
	"""
	icon = StringProperty('')
	"""Unicode character for the icon"""

	width = NumericProperty(dp(48))
	height = NumericProperty(dp(48))

	color_style = OptionProperty(None, options=['Light', 'Dark'], allownone=True)

	def __init__(self, icon='', padding=dp(12), **kwargs):
		super(MaterialIcon, self).__init__(**kwargs)
		self.ripple_color = self._theme_cls.accent_color
		self.padding = padding
		self.icon_label = MaterialLabel(font_style='Icon',
										icon=icon,
										auto_color=self.auto_color,
										color_style=self.color_style)

		self.add_widget(self.icon_label)

	def on_icon(self, instance, value):
		self.icon_label.icon = value


class MaterialButtonBlank(RippleBehavior, ButtonBehavior, MaterialFloatLayout):
	pass

class RaisedButton(ThemeBehaviour, RippleBehavior, ElevationBehaviour, ButtonBehavior, MaterialBoxLayout):

	text = StringProperty()

	color_style = OptionProperty(None, options=['Light', 'Dark'], allownone=True)

	def __init__(self, text='', elevation_normal=2, elevation_raised=0, **kwargs):
		self.text = text
		self.elevation_normal = elevation_normal
		self.elevation_raised = elevation_raised
		self.label = MaterialLabel(font_style='Button',
								   text=text.upper(),
								   auto_color=self.auto_color,
								   color_style=self.color_style,
								   size=self.size,
								   pos=self.pos)
		super(RaisedButton, self).__init__(**kwargs)
		self.background_color = self._theme_cls.primary_color if not self.disabled else self._theme_cls.disabled_color
		self.ripple_color = self._theme_cls.accent_color

		self.add_widget(self.label)
		self.label.bind(size=self._update_text,
						pos=self._update_text,
						text=self._update_text,
						auto_color=self._update_text,
						color_style=self._update_text)

	# def on_disabled(self, instance, value):
	# 	super(RaisedButton, self).on_disabled(instance, value)
	# 	if self.disabled:
	# 		self.background_color = self._theme_cls.disabled_color

	def _update_text(self, *args):
		self.label.auto_color = self.auto_color
		self.label.color_style = self.color_style
		self.label.text = self.text.upper()
		self.label.pos = self.pos
		self.label.size = self.size
		self._update_bg_rectangle_size()
		self._update_bg_rectangle_pos()

	def on_elevation_normal(self, instance, value):
		self.elevation_normal = value

	def on_elevation_raised(self, instance, value):
		self.elevation_raised = value