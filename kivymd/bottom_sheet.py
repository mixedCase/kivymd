# -*- coding: utf-8 -*-
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView
from kivymd.list import List, SingleLineItem
from kivymd.layouts import MaterialBoxLayout


class BottomSheet(MaterialBoxLayout):

	header = StringProperty("")

	def __init__(self, **kwargs):
		self.subheader = SingleLineItem(text=self.header,
		                                size_hint_y=None)
		self.sv = ScrollView(do_scroll_x=False)
		self.list = List()
		super(BottomSheet, self).__init__(**kwargs)
		self.sv.add_widget(self.list)

	def on_header(self, instance, value):
		self.subheader.text = value
		if value == '':
			self.subheader.height = 0
		else:
			self.subheader.height = dp(56)

	def open(self):
		pass

	def dismiss(self):
		pass