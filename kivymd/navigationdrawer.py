# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.uix.image import Image as Image
from kivy.properties import StringProperty, ListProperty, ObjectProperty, AliasProperty
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivymd import material_resources as m_res
from kivymd import images_path
from divider import Divider
from slidingpanel import SlidingPanel
from layouts import MaterialRelativeLayout, MaterialGridLayout, BackgroundColorCapableWidget, MaterialFloatLayout
from label import MaterialLabel
from ripplebehavior import RippleBehavior
from theme import ThemeBehaviour
from material_resources import get_rgba_color

from kivymd.lists import MaterialList

navdrawer_kv = '''
<NavigationDrawer>:
	canvas:
		Color:
			rgba: self._theme_cls.dialog_background_color
		Rectangle:
			size: self.size
			pos: self.pos

	_header_bg: 	header_bg
	_bl_items:		bl_items

	Image:
		id:				header_bg
		source:			root.header_img
		allow_stretch:	True
		size_hint_y:	None
		height:			root.width * 9 / 16
		keep_ratio:		False
		mipmap:			True
		pos:			0, root.height - self.height

	ScrollView:
		do_scroll_x:	False
		size_hint_y:	None
		height:			root.height - header_bg.height

		GridLayout:
			id: 			bl_items
			cols:			1

'''

class NavigationDrawer(ThemeBehaviour, SlidingPanel):
	"""Implementation of the Navigation Drawer pattern."""

	header_img = StringProperty()

	_header_bg = ObjectProperty()
	_bl_items = ObjectProperty()
	def __init__(self, **kwargs):
		Builder.load_string(navdrawer_kv)
		super(NavigationDrawer, self).__init__(**kwargs)
		self.header_img = images_path + "PLACEHOLDER_BG.jpg"

		self._device_rotated('')  # To set self.width properly

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
		if type(widget) == MaterialList:
			self.ids.bl_items.add_widget(widget)

			# self._refresh_list()
			# widget.bind(height=lambda x, y: self._refresh_list())
		else:
			super(NavigationDrawer, self).add_widget(widget, index)

	def remove_widget(self, widget):
		if type(widget) == MaterialList:
			self._bl_items.remove_widget(widget)
			# self._bl_items.add_widget(widget)
			# widget.unbind(height=lambda x, y: self._refresh_list())
		else:
			super(NavigationDrawer, self).remove_widget(widget)

	def on_side(self, instance, value):
		if value != "left":
			raise Exception("Nav drawer can only be on the left side")
#
#
# navdrawercat_kv = '''
# <NavigationDrawerCategory>:
# 	_bl_items:		bl_items
# 	size_hint_y: 	None
#
# 	MaterialLabel:
# 		text:				root._lbl_name
# 		font_style:			'Body2'
# 		theme_text_color:	'Secondary'
# 		size_hint:			1, None
# 		text_size:			self.size
# 		height:				dp(48) if root.name else 0
# 		padding_x:			dp(16)
# 		halign:				'left'
# 		valign:				'middle'
#
# 	GridLayout:
# 		id:					bl_items
# 		cols:				1
# 		size_hint_y:		None
# 		height:				self.minimum_height
#
# 	Divider:
# '''
#
# class NavigationDrawerCategory(ThemeBehaviour, BoxLayout):
# 	name = StringProperty(None, allownone=True)
#
# 	_lbl_name = StringProperty('')
# 	_bl_items = ObjectProperty()
# 	def __init__(self, **kwargs):
# 		Builder.load_string(navdrawercat_kv)
# 		super(NavigationDrawerCategory, self).__init__(**kwargs)
#
# 	def on_name(self, instance, value):
# 		self._lbl_name = value
#
# 	def add_widget(self, widget, index=0):
# 		if type(widget) == NavigationDrawerButton:
# 			self._bl_items.add_widget(widget)
# 			# self._refresh_list()
# 		else:
# 			super(NavigationDrawerCategory, self).add_widget(widget, index)
#
#
# navdrawerbtn_kv = '''
# <NavigationDrawerButton>:
# 	_icon:	icon
# 	_image:	image
# 	canvas:
# 		Color:
# 			rgba: self.background_color_down if self.state == 'down' else (1, 1, 1, 0)
# 		Rectangle:
# 			size: self.size
# 			pos: self.pos
#
#
# 	MaterialLabel:
# 		id: 		icon
# 		font_style:	'Icon'
# 		size_hint:	None, None
# 		width:		0 if not root._icon else dp(24)
# 		height:		0 if not root_icon else dp(24)
#
# 	Image:
# 		id:			image
# 		size_hint:	None, None
# 		size:		0, 0
# 		mipmap:		True
#
# '''
#
# class NavigationDrawerButton(ThemeBehaviour, RippleBehavior, ButtonBehavior, GridLayout):
# 	text = StringProperty()
#
# 	_icon = ObjectProperty(None)
# 	_image = ObjectProperty(None)
#
# 	def _get_icon(self):
# 		return self._icon
#
# 	def _set_icon(self, icon):
# 		if icon[:2] == 'md':
# 			self._icon = MaterialLabel(icon=icon,
# 									   font_style='Icon',
# 									   size_hint=(None, None),
# 									   size=(dp(24), dp(24)),
# 									   pos=(dp(16), dp(12)))
# 		else:
# 			self._icon = Image(size_hint=(None, None),
# 							   size=(dp(24), dp(24)),
# 							   pos=(dp(16), dp(12)),
# 							   mipmap=True,
# 							   source=m_res.ICON_DEFAULT)
#
# 	icon = AliasProperty(_get_icon, _set_icon, bind=('_icon',))
#
# 	background_color_down = ListProperty([])
# 	_tmp_color = ListProperty([])
#
# 	def __init__(self, **kwargs):
# 		self._lbl = MaterialLabel(x=self.x + dp(72),
# 								  font_style='Subhead',
# 								  valign='middle')
# 		super(NavigationDrawerButton, self).__init__(**kwargs)
# 		# self.ripple_color = self._theme_cls.ripple_color
# 		self.background_color_down = get_rgba_color([self._theme_cls.theme_style, 'FlatButtonDown'],
# 													 control_alpha=.4)
# 		self.height = m_res.TOUCH_TARGET_HEIGHT
#
# 		self.add_widget(self._lbl)
# 		self.add_widget(self.icon)
#
# 	def on_text(self, instance, value):
# 		self._lbl.text = value
#
# 	def hide(self):
# 		self.height = dp(0)
#
# 	def on_pos(self, instance, value):
# 		self._icon.pos = (value[0] + dp(16), value[1] + dp(12))
# 		self._lbl.pos = (value[0] + dp(72), value[1])
#
# 	def on_disabled(self, instance, value):
# 		super(FlatButton, self).on_disabled(instance, value)
# 		if self.disabled:
# 			self.label.text_color = self._theme_cls.disabled_color
# 		else:
# 			self.label.text_color = self.text_color
#
# 	def on_state(self, *args):
# 		if self.state == 'down':
# 			self._tmp_color = self.background_color
# 			self.background_color = self._background_color_down
# 		else:
# 			self.background_color = self._tmp_color