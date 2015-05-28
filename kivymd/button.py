# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.properties import StringProperty, NumericProperty, OptionProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivymd.label import MaterialLabel
from kivymd.layouts import MaterialFloatLayout, MaterialBoxLayout
from kivymd.ripplebehavior import RippleBehavior
from kivymd.theme import ThemeBehavior


# class MaterialIcon(ThemeBehavior, RippleBehavior, ButtonBehavior,
#                    MaterialBoxLayout):
# 	"""A 48x48 icon that behaves like a button.
# 	"""
# 	icon = StringProperty()
# 	"""Unicode character for the icon"""
#
# 	width = NumericProperty(dp(48))
# 	height = NumericProperty(dp(48))
#
# 	def __init__(self, icon='', padding=dp(12), **kwargs):
# 		self.padding = padding
# 		self.icon_label = MaterialLabel(font_style="Icon"),
# 		super(MaterialIcon, self).__init__(**kwargs)
# 		self.add_widget(self.icon_label)
#
# 	def on_icon(self, instance, value):
# 		self.icon_label.text = value

class MaterialIcon(ThemeBehavior, RippleBehavior, ButtonBehavior, MaterialBoxLayout):
	"""A 48x48 icon that behaves like a button.
	"""
	icon = StringProperty('')
	"""Unicode character for the icon"""

	width = NumericProperty(dp(48))
	height = NumericProperty(dp(48))

	theme_style = OptionProperty(
		None, options=['Light', 'Dark'], allownone=True)

	def __init__(self, icon='', padding=dp(12), **kwargs):
		super(MaterialIcon, self).__init__(**kwargs)
		self.padding = padding
		self.icon_label = MaterialLabel(
			font_style='Icon',
			icon=icon,
			theme_style=self.theme_style if self.theme_style else \
				App.get_running_app().theme_cls.theme_style)

		if not self.theme_style:
			self.bind(
				theme_style=App.get_running_app().theme_cls.setter(
					'theme_style'))

		self.add_widget(self.icon_label)

	def on_icon(self, instance, value):
		self.icon_label.icon = value

	def on_theme_style(self, instance, style):
		self.theme_style = style


class MaterialButtonBlank(RippleBehavior, ButtonBehavior, MaterialFloatLayout):
	pass