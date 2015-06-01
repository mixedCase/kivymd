# -*- coding: utf-8 -*-

from time import time
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, OptionProperty, ListProperty, BoundedNumericProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.properties import AliasProperty, BooleanProperty
from kivy.metrics import dp, sp
from kivy.uix.switch import Switch
from ripplebehavior import CircularRippleBehavior

from elevationbehaviour import ElevationBehaviour
from kivy.animation import Animation
from material_resources import get_rgba_color, get_icon_char, get_color_tuple
from theme import ThemeBehaviour

txt_chkbox_kv = '''
<MaterialCheckbox>:
	canvas:
		Clear
		Color:
			rgba: self.background_color_disabled if self.disabled else \
			(self.background_color if self.active else self.background_color_down)
		Rectangle:
			size: 		self.size
			pos: 		self.pos
		Color:
			rgba: 		self.color
		Rectangle:
			texture:	self.texture
			size:		self.texture_size
			pos:		int(self.center_x - self.texture_size[0] / 2.), int(self.center_y - self.texture_size[1] / 2.)

	text: 			self._icon_active if self.active else self._icon_normal
	font_name:		'Icons'
	font_size:		sp(24)
	halign:			'center'
	valign:			'middle'

'''
Builder.load_string(txt_chkbox_kv)

class MaterialCheckBox(ThemeBehaviour, CircularRippleBehavior, ToggleButtonBehavior, Label):

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

	active = BooleanProperty(False)

	_icon_normal = StringProperty(u"{}".format(get_icon_char('md-check-box-outline-blank')))
	_icon_active = StringProperty(u"{}".format(get_icon_char('md-check-box')))

	def __init__(self, **kwargs):
		super(MaterialCheckBox, self).__init__(**kwargs)
		self.register_event_type('on_active')
		self.color = self._theme_cls.secondary_text_color()
		self.check_anim_out = Animation(font_size=0, duration=.1, t='out_quad')
		self.check_anim_in = Animation(font_size=sp(24), duration=.1, t='out_quad')
		self.check_anim_in.bind(on_complete=self._set_state)
		self.check_anim_out.bind(on_complete=lambda *x: self.check_anim_in.start(self))

	def on_release(self):
		Animation.cancel_all(self, '_size')
		self.check_anim_out.start(self)

	def _set_state(self, *args):
		if self.state == 'down':
			self.active = True
			self.color = self._theme_cls.primary_color
		else:
			self.active = False
			self.color = self._theme_cls.secondary_text_color()

	def on_active(self, instance, value):
		self.state = 'down' if value else 'normal'


switch_kv = '''
<MaterialSwitch>:
    active_norm_pos: max(0., min(1., (int(self.active) + self.touch_distance / dp(30))))
    canvas:
    	Clear
        Color:
            rgba: self._track_color_disabled if self.disabled else \
            (self._track_color_active if self.active else self._track_color_normal)
		Ellipse:
			size: 			self.height * .6, self.height * .6
			pos:			self.x, self.center_y - (self.height * .6)/2
			angle_start:	180
			angle_end:		360
		Rectangle:
			size:			self.width - (self.height * .6)/2, self.height * .6
			pos:			self.x + (self.height * .6)/2, self.center_y - (self.height * .6)/2
		Ellipse:
			size:			self.height * .6, self.height * .6
			pos:			self.x + self.width - (self.height * .6)/2, self.center_y - (self.height * .6)/2
			angle_start:	0
			angle_end:		180
		Color:
            rgba: self.background_color_disabled if self.disabled else \
            (self.background_color_down if self.active else self.background_color)
        Ellipse:
            size: self.height, self.height
            pos: int(self.center_x - self.height + self.active_norm_pos * dp(30)), int(self.center_y - self.height/2)
'''
Builder.load_string(switch_kv)
class MaterialSwitch(ThemeBehaviour, CircularRippleBehavior, Switch):

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

	_track_color_active = ListProperty()
	_track_color_normal = ListProperty()
	_track_color_disabled = ListProperty()
	def __init__(self, **kwargs):
		super(MaterialSwitch, self).__init__(**kwargs)
		self._track_color_normal = self._theme_cls.hint_text_color()
		if self._theme_cls.theme_style == 'Dark':
			self._track_color_active = self._theme_cls.primary_color
			self._track_color_active[3] = .5
			self._track_color_disabled = get_rgba_color(['Light', 'White'], control_alpha=.1)
			self.background_color = get_rgba_color(['Grey', '400'])
			self.background_color_down = get_rgba_color([self._theme_cls.primary_palette, '200'])
			self.background_color_disabled = get_rgba_color(['Grey', '800'])
		else:
			self._track_color_active = get_rgba_color([self._theme_cls.primary_palette, '200'])
			self._track_color_active[3] = .5
			self._track_color_disabled = self._theme_cls.disabled_bg_color()
			self.background_color = get_rgba_color(['Grey', '50'])
			self.background_color_down = self._theme_cls.primary_color
			self.background_color_disabled = get_rgba_color(['Grey', '400'])

	def _set_ellipse(self, instance, value):
		ellipse = self.ellipse
		ripple_rad = self.ripple_rad
		if ripple_rad > self._finnish_rad * .6:
			self.fade_out()
		ellipse.size = (ripple_rad, ripple_rad)
		ellipse.pos = (int(self.center_x - self.height + self.active_norm_pos * sp(41)), int(self.center_y - self.height/2))