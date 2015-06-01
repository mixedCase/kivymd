# -*- coding: utf-8 -*-

from kivy.metrics import dp
from kivy.properties import AliasProperty

from kivymd.layouts import MaterialRelativeLayout
from theme import ThemeBehaviour


class Divider(ThemeBehaviour, MaterialRelativeLayout):

	def _get_color(self):
		return self.background_color

	def _set_color(self, value):
		self.background_color = value

	color = AliasProperty(_get_color, _set_color, bind=None)

	def __init__(self, **kwargs):
		super(Divider, self).__init__(**kwargs)
		self.color = self._theme_cls.divider_color()
		self.size_hint_y = None
		self.height = dp(1)
