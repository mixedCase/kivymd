# -*- coding: utf-8 -*-

from functools import partial
from kivy.properties import ListProperty, NumericProperty, StringProperty
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
	ripple_rad = NumericProperty(10)
	ripple_pos = ListProperty([0, 0])
	ripple_color = ListProperty()
	ripple_duration_in_fast = NumericProperty(.3)
	ripple_duration_in_slow = NumericProperty(2)
	ripple_duration_out = NumericProperty(.3)
	ripple_fade_to_alpha = NumericProperty(.5)
	ripple_scale = NumericProperty(2.75)
	ripple_func_in = StringProperty('linear')
	ripple_func_out = StringProperty('out_quad')
	ripple_press_timeout = NumericProperty(0.1)

	_duration = NumericProperty()
	def on_touch_down(self, touch):
		if hasattr(self, 'disabled'):
			if not self.disabled:
				if self.collide_point(*touch.pos):
					r_callback = partial(self.start_rippeling, touch)
					touch.ud['ripple_timeout'] = r_callback
					self.anim_complete(self, self)
					self.ripple_pos = ripple_pos = (touch.x, touch.y)
					Animation.cancel_all(self, 'ripple_rad', 'ripple_color',
										 'rect_color')
					ripple_rad = self.ripple_rad
					if hasattr(self, '_theme_cls'):
						self.ripple_color = self._theme_cls.ripple_color
					else:
						self.ripple_color = [rc[0], rc[1], rc[2], .9]

					Clock.schedule_once(r_callback, self.ripple_press_timeout)

					with self.canvas.after:
						StencilPush()
						Rectangle(pos=self.pos, size=self.size)
						StencilUse()
						self.col_instruction = Color(rgba=self.ripple_color)
						self.ellipse = Ellipse(size=(ripple_rad, ripple_rad),
											   pos=(ripple_pos[0] - ripple_rad / 2.,
													ripple_pos[1] - ripple_rad / 2.))
						StencilUnUse()
						Rectangle(pos=self.pos, size=self.size)
						StencilPop()
					self.bind(ripple_color=self.set_color, ripple_pos=self.set_ellipse,
							  ripple_rad=self.set_ellipse)
				return super(RippleBehavior, self).on_touch_down(touch)

	def on_touch_move(self, touch, *args):
		if not self.collide_point(*touch.pos):
			self.finnish_ripple(touch)
		return super(RippleBehavior, self).on_touch_move(touch, *args)

	def on_touch_up(self, touch):
		if self._duration == self.ripple_duration_in_slow:
			self.finnish_ripple(touch)
			return super(RippleBehavior, self).on_touch_up(touch)
		else:
			self.fade_out(touch)
			return super(RippleBehavior, self).on_touch_up(touch)

	def start_rippeling(self, touch, *args):
		rc = self.ripple_color
		self._duration = self.ripple_duration_in_slow if self.state == 'down' else self.ripple_duration_in_fast
		anim = Animation(ripple_rad=max(self.width, self.height) * self.ripple_scale,
						  t=self.ripple_func_in,
						  ripple_color=[rc[0], rc[1], rc[2], self.ripple_fade_to_alpha],
						  duration=self._duration)
		anim.bind(on_complete=self.anim_complete)
		anim.start(self)

	def set_ellipse(self, instance, value):
		ellipse = self.ellipse
		ripple_pos = self.ripple_pos
		ripple_rad = self.ripple_rad
		ellipse.size = (ripple_rad, ripple_rad)
		ellipse.pos = (ripple_pos[0] - ripple_rad / 2.,
					   ripple_pos[1] - ripple_rad / 2.)

	def set_color(self, instance, value):
		self.col_instruction.rgba = value

	def finnish_ripple(self, touch, *args):
		Animation.cancel_all(self, 'ripple_rad')
		anim = Animation(ripple_rad=max(self.width, self.height) * self.ripple_scale,
						  t=self.ripple_func_in,
						  duration=self.ripple_duration_in_fast)
		anim.bind(on_complete=partial(self.fade_out, touch))
		anim.start(self)

	def fade_out(self, touch, *args):
		rc = self.ripple_color
		Animation.cancel_all(self, 'ripple_color')
		anim = Animation(ripple_color=[rc[0], rc[1], rc[2], 0.],
						 t=self.ripple_func_out, duration=self.ripple_duration_out)
		anim.bind(on_complete=self.anim_complete)
		anim.start(self)

	def anim_complete(self, anim, instance, *args):
		self.ripple_rad = 10
		self.canvas.after.clear()