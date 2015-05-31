# -*- coding: utf-8 -*-

from functools import partial
from kivy.properties import ListProperty, NumericProperty, StringProperty, BooleanProperty
from kivy.animation import Animation
from kivy.graphics import Color, Ellipse, StencilPush, StencilPop, StencilUse, \
	StencilUnUse, Rectangle
from kivy.clock import Clock

class RippleBehavior(object):
	""":class:`RippleBehaviour` provides a ripple effect much like the one seen in the
	Material Design by Google. The color of the ripple is by default the same as
	:class:`ThemeManager.accent_color`. Look at the documentation on :class:`ThemeManager`
	for information on how to change it.

	.. note:
		Special thanks to github.com/Kovak/ for his work on FlatKivy, which provided
		the basis for this class.
	"""
	ripple_rad = NumericProperty()
	ripple_rad_default = NumericProperty(1)
	ripple_pos = ListProperty()
	rip_color = ListProperty()
	ripple_duration_in_fast = NumericProperty(.3)
	ripple_duration_in_slow = NumericProperty(2)
	ripple_duration_out = NumericProperty(.5)
	ripple_alpha = NumericProperty(.5)
	ripple_scale = NumericProperty(2.75)
	ripple_func_in = StringProperty('out_quad')
	ripple_func_out = StringProperty('out_quad')

	_duration = NumericProperty()
	_func_in = StringProperty()
	_finnishing = BooleanProperty(False)
	_rippeling = BooleanProperty(False)
	def on_touch_down(self, touch):
		if touch.is_mouse_scrolling:
			return False
		if not self.collide_point(touch.x, touch.y):
			return False
		if hasattr(self, 'disabled'):
			if not self.disabled:
				self.ripple_rad = self.ripple_rad_default
				self.ripple_pos = ripple_pos = (touch.x, touch.y)
				Animation.cancel_all(self, 'ripple_rad', 'ripple_color',
									 'rect_color')
				ripple_rad = self.ripple_rad

				if not hasattr(self, 'ripple_color'):
					self.rip_color = [rc[0], rc[1], rc[2], self.ripple_alpha]
				else:
					self.rip_color = self.ripple_color
					self.rip_color[3] = self.ripple_alpha

				with self.canvas.after:
					StencilPush()
					Rectangle(pos=self.pos, size=self.size)
					StencilUse()
					self.col_instruction = Color(rgba=self.rip_color)
					self.ellipse = Ellipse(size=(ripple_rad, ripple_rad),
										   pos=(ripple_pos[0] - ripple_rad / 2.,
												ripple_pos[1] - ripple_rad / 2.))
					StencilUnUse()
					Rectangle(pos=self.pos, size=self.size)
					StencilPop()
				self.bind(rip_color=self._set_color, ripple_pos=self._set_ellipse,
						  ripple_rad=self._set_ellipse)
				self.start_rippeling(touch)
		return super(RippleBehavior, self).on_touch_down(touch)

	def on_touch_move(self, touch, *args):
		if not self.collide_point(touch.x, touch.y):
			if not self._finnishing and self._rippeling:
				self.finnish_ripple(touch)
		return super(RippleBehavior, self).on_touch_move(touch)

	def on_touch_up(self, touch):
		if self.collide_point(touch.x, touch.y) and self._rippeling:
			self.finnish_ripple(touch)
		return super(RippleBehavior, self).on_touch_up(touch)

	def start_rippeling(self, touch, *args):
		if not self._rippeling:
			anim = Animation(ripple_rad=max(self.width, self.height) * self.ripple_scale,
							 t='linear',
							 duration=self.ripple_duration_in_slow)
			anim.bind(on_complete=self.fade_out)
			self._rippeling = True
			anim.start(self)

	def _set_ellipse(self, instance, value):
		ellipse = self.ellipse
		ripple_pos = self.ripple_pos
		ripple_rad = self.ripple_rad
		ellipse.size = (ripple_rad, ripple_rad)
		ellipse.pos = (ripple_pos[0] - ripple_rad / 2.,
					   ripple_pos[1] - ripple_rad / 2.)

	def _set_color(self, instance, value):
			self.col_instruction.a = value[3]

	def finnish_ripple(self, touch, *args):
		self._finnishing = True
		rc = self.ripple_color
		if self._rippeling:
			Animation.cancel_all(self, 'ripple_rad')
			anim = Animation(ripple_rad=max(self.width, self.height) * self.ripple_scale,
							 t=self.ripple_func_in,
							 duration=self.ripple_duration_in_fast)
			anim.bind(on_complete=self.anim_complete)
			self.fade_out()
			anim.start(self)

	def fade_out(self, *args):
		self._finnishing = True
		rc = self.ripple_color
		if self._rippeling:
			Animation.cancel_all(self, 'rip_color')
			anim = Animation(rip_color=[rc[0], rc[1], rc[2], 0.],
							 t=self.ripple_func_out, duration=self.ripple_duration_out)
			anim.bind(on_complete=self.anim_complete)
			anim.start(self)

	def anim_complete(self, anim, *args):
		self._rippeling = False
		self._finnishing = False
		anim.cancel_all(self)
		self.canvas.after.clear()


class CircularRippleBehavior(object):
	""":class:`CircularRippleBehaviour` provides a ripple effect much like the one seen in the
	Material Design by Google. The color of the ripple is by default the same as
	:class:`ThemeManager.accent_color`. Look at the documentation on :class:`ThemeManager`
	for information on how to change it.

	.. note:
		Special thanks to github.com/Kovak/ for his work on FlatKivy, which provided
		the basis for this class.
	"""
	ripple_rad = NumericProperty()
	ripple_rad_default = NumericProperty(1)
	rip_color = ListProperty()
	ripple_duration_in_fast = NumericProperty(.2)
	ripple_duration_in_slow = NumericProperty(1.5)
	ripple_duration_out = NumericProperty(.2)
	ripple_alpha = NumericProperty(.5)
	ripple_scale = NumericProperty(1)
	ripple_func_in = StringProperty('out_quad')
	ripple_func_out = StringProperty('out_quad')

	_duration = NumericProperty()
	_func_in = StringProperty()
	_finnishing = BooleanProperty(False)
	_rippeling = BooleanProperty(False)
	_fading_out = BooleanProperty(False)
	_finnish_rad = NumericProperty()
	def on_touch_down(self, touch):
		if touch.is_mouse_scrolling:
			return False
		if not self.collide_point(touch.x, touch.y):
			return False

		self.ripple_rad = self.ripple_rad_default
		if hasattr(self, 'disabled'):
			if not self.disabled:
				Animation.cancel_all(self, 'ripple_rad', 'ripple_color',
									 'rect_color')
				ripple_rad = self.ripple_rad

				if not hasattr(self, 'ripple_color'):
					self.rip_color = [rc[0], rc[1], rc[2], self.ripple_alpha]
				else:
					self.rip_color = self.ripple_color
					self.rip_color[3] = self.ripple_alpha

				with self.canvas.after:
					StencilPush()
					Ellipse(size=(self.width * self.ripple_scale,
								  self.height * self.ripple_scale),
							pos=(self.center_x - (self.width * self.ripple_scale)/2,
								 self.center_y - (self.height * self.ripple_scale)/2))
					StencilUse()
					self.col_instruction = Color(rgba=self.rip_color)
					self.ellipse = Ellipse(size=(ripple_rad, ripple_rad),
										   pos=(self.center_x - ripple_rad / 2.,
												self.center_y - ripple_rad / 2.))
					StencilUnUse()
					Ellipse(pos=self.pos, size=self.size)
					StencilPop()
				self.bind(rip_color=self._set_color, ripple_rad=self._set_ellipse)
				self.start_rippeling(touch)
		return super(CircularRippleBehavior, self).on_touch_down(touch)

	def on_touch_move(self, touch, *args):
		if not self.collide_point(touch.x, touch.y):
			if not self._finnishing and self._rippeling:
				self.finnish_ripple(touch)
		return super(CircularRippleBehavior, self).on_touch_move(touch)

	def on_touch_up(self, touch):
		if self.collide_point(touch.x, touch.y) and self._rippeling:
			self.finnish_ripple(touch)
		return super(CircularRippleBehavior, self).on_touch_up(touch)

	def start_rippeling(self, touch, *args):
		self._finnish_rad = max(self.width, self.height) * self.ripple_scale
		if not self._rippeling:
			anim = Animation(ripple_rad=self._finnish_rad,
							 t='linear',
							 duration=self.ripple_duration_in_slow)
			anim.bind(on_complete=self.fade_out)
			self._rippeling = True
			anim.start(self)

	def _set_ellipse(self, instance, value):
		ellipse = self.ellipse
		ripple_rad = self.ripple_rad
		if ripple_rad > self._finnish_rad * .6 and not self.state == 'down':
			self.fade_out()
		ellipse.size = (ripple_rad, ripple_rad)
		ellipse.pos = (self.center_x - ripple_rad / 2.,
					   self.center_y - ripple_rad / 2.)

	def _set_color(self, instance, value):
			self.col_instruction.a = value[3]

	def finnish_ripple(self, touch, *args):
		self._finnishing = True
		if self._rippeling:
			Animation.cancel_all(self, 'ripple_rad')
			anim = Animation(ripple_rad=max(self.width, self.height) * self.ripple_scale,
							  t=self.ripple_func_in,
							  duration=self.ripple_duration_in_fast)
			anim.bind(on_complete=self.fade_out)
			anim.start(self)

	def fade_out(self, *args):
		self._finnishing = True
		rc = self.ripple_color
		if self._rippeling and not self._fading_out:
			Animation.cancel_all(self, 'rip_color')
			anim = Animation(rip_color=[rc[0], rc[1], rc[2], 0.],
							 t=self.ripple_func_out, duration=self.ripple_duration_out)
			anim.bind(on_complete=self.anim_complete)
			self._fading_out = True
			anim.start(self)

	def anim_complete(self, anim, *args):
		self._rippeling = False
		self._finnishing = False
		self._fading_out = False
		anim.cancel_all(self)
		self.canvas.after.clear()