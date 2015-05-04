# -*- coding: utf-8 -*-
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp

from layouts import MaterialFloatLayout, MaterialBoxLayout
from kivymd.label import MaterialLabel
from ripplebehavior import RippleBehavior


class MaterialIcon(RippleBehavior, ButtonBehavior, MaterialBoxLayout):
	"""A 48x48 icon that behaves like a button.
	"""
	icon = StringProperty()
	"""Unicode character for the icon"""

	width = NumericProperty(dp(48))
	height = NumericProperty(dp(48))

	def __init__(self, icon='', padding=dp(12), **kwargs):
		self.padding = padding
		self.icon_label = MaterialLabel(style="icon",
										font_size=dp(24))
		super(MaterialIcon, self).__init__(**kwargs)
		self.add_widget(self.icon_label)

	def on_icon(self, instance, value):
		self.icon_label.text = value


class MaterialButtonBlank(RippleBehavior, ButtonBehavior, MaterialFloatLayout):
	pass