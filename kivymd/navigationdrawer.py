# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.image import Image as Image
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView

from kivymd import material_resources as m_res
from divider import Divider
from slidingpanel import SlidingPanel
from layouts import MaterialRelativeLayout, MaterialGridLayout, BackgroundColorCapableWidget
from label import MaterialLabel
from button import MaterialButtonBlank
from theme import ThemeBehaviour


class NavigationDrawer(ThemeBehaviour, SlidingPanel, BackgroundColorCapableWidget):
	"""Implementation of the Navigation Drawer pattern."""

	header_img = StringProperty()

	def __init__(self, header_img='', **kwargs):
		self.scroll_view = ScrollView(do_scroll_x=False,
									  size_hint_y=None)
		self._bl_items = MaterialGridLayout(size_hint_y=None,
											spacing=dp(8),
											cols=1,
											height=0)
		self._header_bg = Image(allow_stretch=True,
								size_hint_y=None,
								keep_ratio=False,
								mipmap=True)
		super(NavigationDrawer, self).__init__(**kwargs)
		self.background_color = self._theme_cls.dialog_background_color
		self.header_img = header_img
		self._header_bg.height = self.width * 9 / 16
		self.header_divider = Divider()
		self._header_bg.bind(width=self.header_divider.setter('width'),
							 pos=self.header_divider.setter('pos'))

		self.add_widget(self._header_bg)
		# TODO: Add header layout here, don't forger horiz margin
		self.add_widget(self.header_divider)
		self.add_widget(self.scroll_view)
		self.scroll_view.add_widget(self._bl_items)

		self._device_rotated('')  # To set self.width properly

	def on_header_img(self, instance, value):
		self._header_bg.source = value

	def on_height(self, instance, value):
		self._header_bg.y = value - self._header_bg.height
		self.scroll_view.height = value - self._header_bg.height - dp(8)

	def on_width(self, instance, value):
		self._header_bg.height = value * 9 / 16
		self._header_bg.width = value
		self._bl_items.width = value - m_res.HORIZ_MARGINS

	def _define_width(self):
		if (Window.width - m_res.STANDARD_INCREMENT) < \
				m_res.MAX_NAV_DRAWER_WIDTH:
			self.width = Window.width - m_res.STANDARD_INCREMENT
		else:
			self.width = m_res.MAX_NAV_DRAWER_WIDTH

	def _device_rotated(self, orientation):
		old_width = self.width
		self._define_width()
		if self.status == "closed":
			self.x -= self.width - old_width
		super(NavigationDrawer, self)._device_rotated(orientation)

	def add_widget(self, widget, index=0):
		if type(widget) == NavigationDrawerCategory or \
						type(widget) == NavigationDrawerButton:
			self._bl_items.add_widget(widget)
			self._refresh_list()
			widget.bind(height=lambda x, y: self._refresh_list())
		else:
			super(NavigationDrawer, self).add_widget(widget, index)

	def remove_widget(self, widget):
		if type(widget) == NavigationDrawerCategory or \
						type(widget) == NavigationDrawerButton:
			self._bl_items.remove_widget(widget)
			self._bl_items.add_widget(widget)
			widget.unbind(height=lambda x, y: self._refresh_list())
		else:
			super(NavigationDrawer, self).remove_widget(widget)

	def _refresh_list(self):
		item_list_height = 0
		for i in self._bl_items.children:
			item_list_height += i.height
			item_list_height += self._bl_items.spacing[1]
		self._bl_items.height = item_list_height

	def on_side(self, instance, value):
		if value != "left":
			raise Exception("Nav drawer can only be on the left side")


class NavigationDrawerCategory(ThemeBehaviour, MaterialRelativeLayout, BackgroundColorCapableWidget):
	name = StringProperty('Category')
	divider = BooleanProperty(True)
	subheader = BooleanProperty(True)

	def __init__(self, **kwargs):
		self._lbl_name = MaterialLabel(size_hint_y=None,
									   text=self.name,
									   x=dp(16),
									   height=dp(48),
									   font_style='Title',
									   auto_color=True)
		self.bind(name=self._lbl_name.setter('text'))
		self._bl_items = MaterialGridLayout(orientation="vertical",
											size_hint_y=None,
											height=0,
											pos=(0, 0),
											cols=1)
		self._divider = Divider()
		super(NavigationDrawerCategory, self).__init__(**kwargs)
		self.add_widget(self._lbl_name)

		self.add_widget(self._bl_items)
		self.add_widget(self._divider)

		self.size_hint_y = None
		self.height = self._lbl_name.height

	def on_name(self, instance, value):
		self._lbl_name.text = value

	def on_subheader(self, instance, value):
		if value:
			self._lbl_name.height = dp(48)
			self._lbl_name.opacity = 100
		else:
			self._lbl_name.height = dp(0)
			self._lbl_name.opacity = 0

	def on_divider(self, instance, value):
		if value:
			self._divider.opacity = 100
		else:
			self._divider.opacity = 0

	def on_height(self, instance, value):
		self._lbl_name.y = value - self._lbl_name.height
		self._bl_items.y = value - self._lbl_name.height - \
						   self._bl_items.height

	def on_width(self, instance, value):
		self._divider.width = value

	def add_widget(self, widget, index=0):
		if type(widget) == NavigationDrawerButton:
			self._bl_items.add_widget(widget)
			self._refresh_list()
		else:
			super(NavigationDrawerCategory, self).add_widget(widget, index)

	def _refresh_list(self):
		item_list_height = 0
		for i in self._bl_items.children:
			item_list_height += i.height
		self._bl_items.height = item_list_height
		self.height = self._lbl_name.height + item_list_height


class NavigationDrawerButton(ThemeBehaviour, MaterialButtonBlank, BackgroundColorCapableWidget):
	text = StringProperty()

	def __init__(self, **kwargs):
		self._lbl = MaterialLabel(x=self.x + dp(72),
								  font_style='Subhead',
								  auto_color=True)
		super(NavigationDrawerButton, self).__init__(**kwargs)
		self.ripple_color = self._theme_cls.accent_color

		self.height = m_res.TOUCH_TARGET_HEIGHT

		self._icon = Image(size_hint=(None, None),
						   size=(dp(24), dp(24)),
						   pos=(dp(16), dp(12)),
						   mipmap=True,
						   source=m_res.ICON_DEFAULT)
		self.add_widget(self._lbl)
		self.add_widget(self._icon)

	def on_text(self, instance, value):
		self._lbl.text = value

	def hide(self):
		self.height = dp(0)

	def on_pos(self, instance, value):
		self._icon.pos = (value[0] + dp(16), value[1] + dp(12))
		self._lbl.pos = (value[0] + dp(72), value[1])
