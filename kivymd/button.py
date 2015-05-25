# -*- coding: utf-8 -*-

from kivy.properties import StringProperty, NumericProperty, OptionProperty, ListProperty, BoundedNumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import AliasProperty
from kivy.metrics import dp
from layouts import MaterialFloatLayout, MaterialBoxLayout
from kivymd.label import MaterialLabel
from ripplebehavior import RippleBehavior
from elevationbehaviour import ElevationBehaviour
from kivy.animation import Animation
from material_resources import get_rgba_color, get_btn_down_color

from theme import ThemeBehaviour

class MaterialIcon(ThemeBehaviour, RippleBehavior, ButtonBehavior, MaterialBoxLayout):
	"""A 48x48 icon that behaves like a button.
	"""
	icon = StringProperty('')
	"""Unicode character for the icon"""

	width = NumericProperty(dp(48))
	height = NumericProperty(dp(48))

	theme_style = OptionProperty(None, options=['Light', 'Dark'], allownone=True)

	def __init__(self, icon='', padding=dp(12), **kwargs):
		super(MaterialIcon, self).__init__(**kwargs)
		self.ripple_color = self._theme_cls.ripple_color
		self.padding = padding
		self.icon_label = MaterialLabel(font_style='Icon',
										icon=icon,
										theme_style=self.theme_style if self.theme_style else self._theme_cls.theme_style)

		if not self.theme_style:
			self.bind(theme_style=self._theme_cls.setter('theme_style'))

		self.add_widget(self.icon_label)

	def on_icon(self, instance, value):
		self.icon_label.icon = value

	def on_theme_style(self, instance, style):
		self.theme_style = style


class MaterialButtonBlank(RippleBehavior, ButtonBehavior, MaterialFloatLayout):
	pass

class FlatButton(ThemeBehaviour, RippleBehavior, ButtonBehavior, MaterialBoxLayout):

	text = StringProperty('')

	text_color = ListProperty(None, allownone=True)

	_background_color_down = ListProperty([])

	def _get_bg_color_down(self):
		return self._background_color_down

	def _set_bg_color_down(self, color):
		if len(color) == 2:
			self._background_color_down = get_rgba_color(color)
		elif len(color) == 3 or len(color) == 4:
			self._background_color_down = color

	background_color_down = AliasProperty(_get_bg_color_down, _set_bg_color_down,
										  bind=('_background_color_down', ))

	_tmp_color = ListProperty([])

	def __init__(self, **kwargs):
		self.label = MaterialLabel(font_style='Button',
								   theme_style='Custom',
								   size=self.size,
								   pos=self.pos)
		super(FlatButton, self).__init__(**kwargs)
		self.label.text_color = self.text_color if self.text_color else self._theme_cls.primary_text_color()
		self.ripple_color = self._theme_cls.ripple_color

		self._tmp_color = self.background_color
		self._background_color_down = get_rgba_color([self._theme_cls.theme_style, 'FlatButtonDown'],
													 control_alpha=.4)
		self.add_widget(self.label)

	def on_touch_down(self, touch):
		if touch.is_mouse_scrolling:
			return False
		if not self.collide_point(touch.x, touch.y):
			return False
		if self in touch.ud:
			return False
		if not self.disabled:
			self._tmp_color = self.background_color
			self.background_color = self._background_color_down
		super(FlatButton, self).on_touch_down(touch)

	def on_touch_up(self, touch):
		if not self.disabled:
			if touch.grab_current is not self:
				return super(ButtonBehavior, self).on_touch_up(touch)
			self.background_color = self._tmp_color
			super(FlatButton, self).on_touch_up(touch)

	def on_size(self, instance, size):
		self.size = size
		self.label.size = size
		if hasattr(self, '_bg_rect'):
			self._update_bg_rectangle_size()
			self._update_bg_rectangle_pos()


	def on_pos(self, instance, pos):
		self.pos = pos
		self.label.pos = pos
		if hasattr(self, '_bg_rect'):
			self._update_bg_rectangle_size()
			self._update_bg_rectangle_pos()


	def on_text(self, instance, text):
		self.label.text = text.upper()

class RaisedButton(ThemeBehaviour, RippleBehavior, ElevationBehaviour, ButtonBehavior, MaterialBoxLayout):

	elevation_normal = BoundedNumericProperty(2, min=0, max=12)
	elevation_raised = BoundedNumericProperty(0, min=0, max=12)

	text = StringProperty()

	theme_style = OptionProperty(None, options=['Light', 'Dark', 'Custom'], allownone=True)

	text_color = ListProperty(None, allownone=True)

	_background_color_down = ListProperty()

	def __init__(self, text='', elevation_normal=2, elevation_raised=0, **kwargs):
		self.text = text
		self.elevation = elevation_normal
		self.elevation_normal = elevation_normal
		self.elevation_raised = elevation_raised
		if self.elevation_raised == 0 and self.elevation_normal + 6 <= 12:
			self.elevation_raised = self.elevation_normal + 6
		elif self.elevation_raised == 0:
			self.elevation_raised = 12

		self.label = MaterialLabel(font_style='Button',
								   text=text.upper(),
								   size=self.size,
								   pos=self.pos)

		super(RaisedButton, self).__init__(**kwargs)
		self.label.theme_style = self.theme_style if self.theme_style else self._theme_cls.theme_style
		self.label.bind(theme_style=self.setter('theme_style'),
						text_color=self.setter('text_color'),
						text=self.setter('text'))

		self.elevation_press_anim = Animation(elevation=self.elevation_raised, duration=.2, t='out_quad')
		self.elevation_release_anim = Animation(elevation=self.elevation_normal, duration=.2, t='out_quad')
		self.background_color = self._theme_cls.primary_color if not self.disabled else self._theme_cls.disabled_bg_color()
		if not self.disabled:
			self._background_color_down = get_btn_down_color(self.background_color)
		self.ripple_color = self._theme_cls.ripple_color

		self.add_widget(self.label)
		self.bind(size=self._update,
				  pos=self._update)

	def on_disabled(self, instance, value):
		super(RaisedButton, self).on_disabled(instance, value)
		if self.disabled:
			self.background_color = self._theme_cls.disabled_bg_color()
			self.elevation = 0
		else:
			self.background_color = self._theme_cls.primary_color
			self._background_color_down = get_btn_down_color(self.background_color)
			self.elevation = self.elevation_normal

	def on_touch_down(self, touch):
		if not self.disabled:
			if touch.is_mouse_scrolling:
				return False
			if not self.collide_point(touch.x, touch.y):
				return False
			if self in touch.ud:
				return False
			self.background_color = self._background_color_down
			self.elevation_press_anim.stop(self)
			self.elevation_press_anim.start(self)
			super(RaisedButton, self).on_touch_down(touch)

	def on_touch_up(self, touch):
		if not self.disabled:
			if touch.grab_current is not self:
				return super(ButtonBehavior, self).on_touch_up(touch)
			self.background_color = self._theme_cls.primary_color
			self.elevation_release_anim.stop(self)
			self.elevation_release_anim.start(self)
			super(RaisedButton, self).on_touch_up(touch)

	def _update(self, *args):
		self.label.texture_update()
		self.label.pos = self.pos
		self.label.size = self.size
		self._update_bg_rectangle_size()
		self._update_bg_rectangle_pos()


	def on_text(self, instance, text):
		self.label.text = text.upper()

	def on_elevation_normal(self, instance, value):
		self.elevation = value

	def on_elevation_raised(self, instance, value):
		if self.elevation_raised == 0 and self.elevation_normal + 6 <= 12:
			self.elevation_raised = self.elevation_normal + 6
		elif self.elevation_raised == 0:
			self.elevation_raised = 12