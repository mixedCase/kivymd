# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.properties import (StringProperty, OptionProperty,
							 ListProperty, BoundedNumericProperty, ObjectProperty)
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import AliasProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.label import MaterialLabel
from ripplebehavior import RippleBehavior, CircularRippleBehavior
from elevationbehaviour import ElevationBehaviour
from kivy.animation import Animation
from material_resources import get_rgba_color

from theme import ThemeBehaviour

materialiconbtn_kv = '''
<MaterialIconButton>:
	canvas:
		Color:
			rgba: self.background_color_disabled if self.disabled else \
			(self.background_color if self.state == 'normal' else self.background_color_down)
		Rectangle:
			size: self.size
			pos: self.pos

	padding:	dp(12), dp(12)
	font_style:	'Icon'
	text_size:	self.size

'''
Builder.load_string(materialiconbtn_kv)
class MaterialIconButton(CircularRippleBehavior, ButtonBehavior, MaterialLabel):
	"""A 48x48 icon that behaves like a button.
	"""
	_bg_color_down = ListProperty([1, 1, 1, 0])
	def _get_bg_color_down(self):
		return self._bg_color_down

	def _set_bg_color_down(self, color, alpha=None):
		if len(color) == 2:
			self._bg_color_down = get_rgba_color(color, control_alpha=alpha)
		elif len(color) == 4:
			self._bg_color_down = color

	background_color_down = AliasProperty(_get_bg_color_down, _set_bg_color_down,
										  bind=('_bg_color_down', ))

	_bg_color_disabled = ListProperty([1, 1, 1, 0])
	def _get_bg_color_disabled(self):
		return self._bg_color_disabled

	def _set_bg_color_disabled(self, color, alpha=None):
		if len(color) == 2:
			self._bg_color_disabled = get_rgba_color(color, control_alpha=alpha)
		elif len(color) == 4:
			self._bg_color_disabled = color
	background_color_disabled = AliasProperty(_get_bg_color_disabled, _set_bg_color_disabled,
											  bind=('_bg_color_disabled', ))

	theme_style = OptionProperty(None, options=['Light', 'Dark'], allownone=True)

	def __init__(self, **kwargs):
		super(MaterialIconButton, self).__init__(**kwargs)


class MaterialButtonBlank(RippleBehavior, ButtonBehavior, FloatLayout):
	pass

flatbutton_kv = '''
<FlatButton>
	canvas:
		Color:
			rgba: self.background_color_disabled if self.disabled else \
			(self.background_color if self.state == 'normal' else self.background_color_down)
		Rectangle:
			size: self.size
			pos: self.pos

	_label:				label
	anchor_x:			'center'
	anchor_y:			'center'

	MaterialLabel:
		id:				label
		font_style: 	'Button'
		text:			root._text
		size_hint:		None, None
		text_size:	 	None, None
		size:			self.texture_size
		theme_style:	'Custom'
		text_color:		root.text_color if root.state == 'normal' else root.text_color_down
		disabled:		root.disabled
		halign: 		'center'
		valign: 		'middle'

'''
Builder.load_string(flatbutton_kv)
class FlatButton(ThemeBehaviour, RippleBehavior, ButtonBehavior, AnchorLayout):

	text = StringProperty('')

	text_color = ListProperty()

	text_color_down = ListProperty()

	_bg_color_down = ListProperty([])
	def _get_bg_color_down(self):
		return self._bg_color_down

	def _set_bg_color_down(self, color, alpha=None):
		if len(color) == 2:
			self._bg_color_down = get_rgba_color(color, control_alpha=alpha)
		elif len(color) == 4:
			self._bg_color_down = color

	background_color_down = AliasProperty(_get_bg_color_down, _set_bg_color_down,
										  bind=('_bg_color_down', ))

	_bg_color_disabled = ListProperty([])
	def _get_bg_color_disabled(self):
		return self._bg_color_disabled

	def _set_bg_color_disabled(self, color, alpha=None):
		if len(color) == 2:
			self._bg_color_disabled = get_rgba_color(color, control_alpha=alpha)
		elif len(color) == 4:
			self._bg_color_disabled = color
	background_color_disabled = AliasProperty(_get_bg_color_disabled, _set_bg_color_disabled,
											  bind=('_bg_color_disabled', ))
	_label = ObjectProperty()
	def _get_bg_color_down(self):
		return self._bg_color_down

	def _set_bg_color_down(self, color, alpha=None):
		if len(color) == 2:
			self._bg_color_down = get_rgba_color(color, control_alpha=alpha)
		elif len(color) == 4:
			self._bg_color_down = color

	background_color_down = AliasProperty(_get_bg_color_down, _set_bg_color_down,
										  bind=('_bg_color_down', ))

	_bg_color_disabled = ListProperty([])
	def _get_bg_color_disabled(self):
		return self._bg_color_disabled

	def _set_bg_color_disabled(self, color, alpha=None):
		if len(color) == 2:
			self._bg_color_disabled = get_rgba_color(color, control_alpha=alpha)
		elif len(color) == 4:
			self._bg_color_disabled = color
	background_color_disabled = AliasProperty(_get_bg_color_disabled, _set_bg_color_disabled,
											  bind=('_bg_color_disabled', ))

	theme_style = OptionProperty(None, options=['Light', 'Dark', 'Custom'], allownone=True)

	_text = StringProperty('')
	def __init__(self, **kwargs):
		super(FlatButton, self).__init__(**kwargs)
		self.text_color = self._theme_cls.primary_text_color()
		self.bind(text_color=self.setter('text_color_down'))
		self.background_color_down = get_rgba_color([self._theme_cls.theme_style, 'FlatButtonDown'],
													 control_alpha=.4)
		self.background_color_disabled = self._theme_cls.disabled_bg_color()

	def on_text(self, instance, text):
		self._text = text.upper()

raised_btn_kv = '''
<RaisedButton>:
	canvas:
		Clear
		Color:
			rgba: self.background_color_disabled if self.disabled else \
			(self.background_color if self.state == 'normal' else self.background_color_down)
		Rectangle:
			size: self.size
			pos: self.pos

	anchor_x:			'center'
	anchor_y:			'center'
	MaterialLabel:
		id: label
		font_style: 	'Button'
		text:			root._text
		size_hint:		None, None
		width:			root.width
		text_size:		self.width, None
		height:			self.texture_size[1]
		theme_style:	root.theme_style
		text_color:		root.text_color
		disabled:		root.disabled
'''
Builder.load_string(raised_btn_kv)

class RaisedButton(ThemeBehaviour, RippleBehavior, ElevationBehaviour, ButtonBehavior, AnchorLayout):

	_bg_color_down = ListProperty([])
	def _get_bg_color_down(self):
		return self._bg_color_down

	def _set_bg_color_down(self, color, alpha=None):
		if len(color) == 2:
			self._bg_color_down = get_rgba_color(color, control_alpha=alpha)
		elif len(color) == 4:
			self._bg_color_down = color

	background_color_down = AliasProperty(_get_bg_color_down, _set_bg_color_down,
										  bind=('_bg_color_down', ))

	_bg_color_disabled = ListProperty([])
	def _get_bg_color_disabled(self):
		return self._bg_color_disabled

	def _set_bg_color_disabled(self, color, alpha=None):
		if len(color) == 2:
			self._bg_color_disabled = get_rgba_color(color, control_alpha=alpha)
		elif len(color) == 4:
			self._bg_color_disabled = color
	background_color_disabled = AliasProperty(_get_bg_color_disabled, _set_bg_color_disabled,
											  bind=('_bg_color_disabled', ))

	theme_style = OptionProperty(None, options=['Light', 'Dark', 'Custom'], allownone=True)

	text_color = ListProperty(None, allownone=True)


	elevation_normal = BoundedNumericProperty(2, min=0, max=12)
	elevation_raised = BoundedNumericProperty(0, min=0, max=12)

	text = StringProperty()

	_text = StringProperty()

	def __init__(self, **kwargs):
		self.elevation = self.elevation_normal

		if self.elevation_raised == 0 and self.elevation_normal + 6 <= 12:
			self.elevation_raised = self.elevation_normal + 6
		elif self.elevation_raised == 0:
			self.elevation_raised = 12

		super(RaisedButton, self).__init__(**kwargs)
		self.background_color = self._theme_cls.primary_color
		self.background_color_down = self._theme_cls.primary_dark
		self.background_color_disabled = self._theme_cls.disabled_bg_color()


		self.elevation_press_anim = Animation(elevation=self.elevation_raised, duration=.2, t='out_quad')
		self.elevation_release_anim = Animation(elevation=self.elevation_normal, duration=.2, t='out_quad')


	def on_disabled(self, instance, value):
		super(RaisedButton, self).on_disabled(instance, value)
		if self.disabled:
			self.elevation = 0
		else:
			self.elevation = self.elevation_normal

	def on_touch_down(self, touch):
		if not self.disabled:
			if touch.is_mouse_scrolling:
				return False
			if not self.collide_point(touch.x, touch.y):
				return False
			if self in touch.ud:
				return False
			self.elevation_press_anim.stop(self)
			self.elevation_press_anim.start(self)
		return super(RaisedButton, self).on_touch_down(touch)

	def on_touch_up(self, touch):
		if not self.disabled:
			if touch.grab_current is not self:
				return super(ButtonBehavior, self).on_touch_up(touch)
			self.elevation_release_anim.stop(self)
			self.elevation_release_anim.start(self)
		return super(RaisedButton, self).on_touch_up(touch)

	def on_text(self, instance, text):
		self._text = text.upper()

	def on_elevation_normal(self, instance, value):
		self.elevation = value

	def on_elevation_raised(self, instance, value):
		if self.elevation_raised == 0 and self.elevation_normal + 6 <= 12:
			self.elevation_raised = self.elevation_normal + 6
		elif self.elevation_raised == 0:
			self.elevation_raised = 12