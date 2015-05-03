# -*- coding: utf-8 -*-
import material_resources as m_res
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.metrics import sp
from layouts import BackgroundColorCapableWidget


class MaterialLabel(Label, BackgroundColorCapableWidget):
	style = StringProperty("regular")

	def __init__(self, color=(1,1,1,1), **kwargs):
		self.font_size = sp(14)
		super(MaterialLabel, self).__init__(**kwargs)
		self.size_hint_x = None
		self.color = color

	def on_style(self, instance, value):
		if value == "bold":
			self.font_name = m_res.FONT_BOLD
		elif value == "medium":
			self.font_name = m_res.FONT_MEDIUM
		elif value == "regular":
			self.font_name = m_res.FONT_REGULAR
		elif value == "icon":
			self.font_name = m_res.FONT_ICONS
		else:
			raise ValueError("Valid style values are 'regular', 'medium', "
			                 "'bold' and 'icon'")

	def on_texture_size(self, instance, value):
		self.width = value[0]
