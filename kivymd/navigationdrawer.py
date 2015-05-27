# -*- coding: utf-8 -*-

from kivy.uix.image import Image as Image
from kivy.properties import StringProperty, BooleanProperty, ListProperty, ObjectProperty, AliasProperty
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView

from kivymd import material_resources as m_res
from divider import Divider
from slidingpanel import SlidingPanel
from layouts import MaterialRelativeLayout, MaterialGridLayout, BackgroundColorCapableWidget, MaterialFloatLayout
from label import MaterialLabel
from button import MaterialButtonBlank
from theme import ThemeBehaviour
from material_resources import get_rgba_color, get_icon_char

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
			# self._bl_items.add_widget(widget)
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
	name = StringProperty('')

	divider = BooleanProperty(True)
	subheader = BooleanProperty(True)

	def __init__(self, **kwargs):
		self._lbl_name = MaterialLabel(size_hint_y=None,
									   padding_x=dp(16),
									   size=(0, 0),
									   font_style='Title',
									   valign='top',
									   x=0)
		self._lbl_name.bind(texture_size=self._fix_lbl)
		self._bl_items = MaterialGridLayout(orientation="vertical",
											size_hint_y=None,
											height=0,
											cols=1,
											x=0)
		self._divider = Divider()
		super(NavigationDrawerCategory, self).__init__(**kwargs)
		self.add_widget(self._lbl_name)
		self.add_widget(self._bl_items)
		self.add_widget(self._divider)

		self.size_hint_y = None
		self.height = self._lbl_name.height

	def _fix_lbl(self, *args):
		self._lbl_name.texture_update()
		self._lbl_name.text_size = (self._lbl_name.width, None)
		self._lbl_name.height = self._lbl_name.texture_size[1] + dp(50)
		self._refresh_list()

	def on_name(self, instance, value):
		self._lbl_name.text = value

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

	_icon = ObjectProperty(None)
	def _get_icon(self):
		if self._icon:
			return self._icon
		else:
			self._icon = Image(size_hint=(None, None),
							   size=(dp(24), dp(24)),
							   pos=(dp(16), dp(12)),
							   mipmap=True,
							   source=m_res.ICON_DEFAULT)
			return self._icon

	def _set_icon(self, icon):
		if icon[:2] == 'md':
			self._icon = MaterialLabel(icon=icon,
									   font_style='Icon',
									   size_hint=(None, None),
									   size=(dp(24), dp(24)),
									   pos=(dp(16), dp(12)))
		else:
			self._icon = Image(size_hint=(None, None),
							   size=(dp(24), dp(24)),
							   pos=(dp(16), dp(12)),
							   mipmap=True,
							   source=m_res.ICON_DEFAULT)

	icon = AliasProperty(_get_icon, _set_icon, bind=('_icon',))

	_background_color_down = ListProperty([])
	_tmp_color = ListProperty([])

	def __init__(self, **kwargs):
		self._lbl = MaterialLabel(x=self.x + dp(72),
								  font_style='Subhead',
								  valign='middle')
		super(NavigationDrawerButton, self).__init__(**kwargs)
		self.ripple_color = self._theme_cls.ripple_color
		self._background_color_down = get_rgba_color([self._theme_cls.theme_style, 'FlatButtonDown'],
													 control_alpha=.4)
		self.height = m_res.TOUCH_TARGET_HEIGHT

		self.add_widget(self._lbl)
		self.add_widget(self.icon)

	def on_text(self, instance, value):
		self._lbl.text = value

	def hide(self):
		self.height = dp(0)

	def on_pos(self, instance, value):
		self._icon.pos = (value[0] + dp(16), value[1] + dp(12))
		self._lbl.pos = (value[0] + dp(72), value[1])

	def on_disabled(self, instance, value):
		super(FlatButton, self).on_disabled(instance, value)
		if self.disabled:
			self.label.text_color = self._theme_cls.disabled_color
		else:
			self.label.text_color = self.text_color

	def on_state(self, *args):
		if self.state == 'down':
			self._tmp_color = self.background_color
			self.background_color = self._background_color_down
		else:
			self.background_color = self._tmp_color