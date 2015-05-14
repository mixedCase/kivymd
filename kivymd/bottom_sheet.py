# -*- coding: utf-8 -*-
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView
from kivymd.list import List, SubheaderLineItem, SingleLineItem
from kivymd.slidingmodal import ExpandableSlidingModal


class BottomSheet(ExpandableSlidingModal):

	header = StringProperty("Title")

	def __init__(self, **kwargs):
		self.orientation = "vertical"
		self.side = "bottom"
		self.background_color = (1,1,1,1)
		self.subheader = SubheaderLineItem(text=self.header,
		                                   size_hint_y=None,
		                                   divider=False)
		self.sv = ScrollView(do_scroll_x=False,
		                     effect_cls="ScrollEffect")
		self.list = List()
		self.size_hint_y = None
		super(BottomSheet, self).__init__(**kwargs)
		self.on_header(None, self.header)
		self.max_height = Window.height
		Window.bind(on_width=self.setter("width"))
		self.sv.add_widget(self.list)
		self.add_widget(self.subheader)
		self.add_widget(self.sv)


	def on_header(self, instance, value):
		self.subheader.text = value
		if value == '':
			self.subheader.height = 0
		else:
			self.subheader.height = dp(56)

	def open(self):
		self.height = min(self.subheader.height + self.list.height,
		                  4*dp(48) + dp(8))
		self.min_height = self.height
		super(BottomSheet, self).open()

	def resizing_condition(self, new_height):
		if new_height < self.height and self.height == self.max_height and \
						self.sv.scroll_y != 1.:
			return False
		elif self.height < self.max_height:
			self.sv.do_scroll_y = False
			return True
		else:
			self.sv.do_scroll_y = True
			return True

	def add_item(self, widget):
		widget.bind(on_release=lambda x: self.dismiss())
		self.list.add_widget(widget)

	def remove_item(self, widget):
		self.list.remove_widget(widget)

	def on_touch_down(self, touch):
		self._set_touch_down_attr(touch)
		if self.sv.collide_point(*touch.pos):
			self._touch = touch
			return True
		else:
			self._touch = None
		return super(BottomSheet, self).on_touch_down(touch)

	def on_touch_up(self, touch):
		if self._touch and not self._moved:
			return super(BottomSheet, self).on_touch_down(touch)
		return super(BottomSheet, self).on_touch_up(touch)
