# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.animation import Animation
from kivy.graphics import Color, Ellipse, StencilPush, StencilPop, StencilUse,\
	StencilUnUse, Rectangle


class RippleBehavior(object):
	# 	""":class:`RippleBehaviour` provides a ripple effect much like the one seen in the
	# 	Material Design by Google. The color of the ripple is by default the same as
	# 	:class:`ThemeManager.accent_color`. Look at the documentation on :class:`ThemeManager`
	# 	for information on how to change it.
	#
	# 	.. note:
	# 		Special thanks to github.com/Kovak/ for his work on FlatKivy, which provided
	# 		the basis for this class.
	# 	"""
	ripple_rad = NumericProperty(10)
	ripple_pos = ListProperty([0, 0])
	ripple_color = ListProperty()
	ripple_duration_in = NumericProperty(.3)
	ripple_duration_out = NumericProperty(.5)
	ripple_fade_to_alpha = NumericProperty(.7)
	ripple_scale = NumericProperty(2.75)
	ripple_func_in = StringProperty('linear')
	ripple_func_out = StringProperty('out_quad')

	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			self.anim_complete(self, self)
			self.ripple_pos = ripple_pos = (touch.x, touch.y)
			Animation.cancel_all(self, 'ripple_rad', 'ripple_color',
			                     'rect_color')
			if hasattr(App.get_running_app(), 'theme_cls'):
				self.ripple_color = \
					App.get_running_app().theme_cls.ripple_color
			elif self.ripple_color == []:
				raise ValueError("You must set ripple_color if you're not"
				                 " using a ThemeManager")
			ripple_rad = self.ripple_rad
			rc = self.ripple_color
			self.ripple_color = [rc[0], rc[1], rc[2], .9]
			anim = Animation(
				ripple_rad=max(self.width, self.height) * self.ripple_scale,
				t=self.ripple_func_in,
				ripple_color=[rc[0], rc[1], rc[2], self.ripple_fade_to_alpha],
				duration=self.ripple_duration_in)
			anim.start(self)
			with self.canvas.after:
				StencilPush()
				Rectangle(pos=self.pos, size=self.size)
				StencilUse()
				self.col_instruction = Color(rgba=self.ripple_color)
				self.ellipse = Ellipse(size=(ripple_rad, ripple_rad),
				                       pos=(ripple_pos[0] - ripple_rad/2.,
				                            ripple_pos[1] - ripple_rad/2.))
				StencilUnUse()
				Rectangle(pos=self.pos, size=self.size)
				StencilPop()
			self.bind(ripple_color=self.set_color, ripple_pos=self.set_ellipse,
			          ripple_rad=self.set_ellipse)
		return super(RippleBehavior, self).on_touch_down(touch)

	def set_ellipse(self, instance, value):
		ellipse = self.ellipse
		ripple_pos = self.ripple_pos
		ripple_rad = self.ripple_rad
		ellipse.size = (ripple_rad, ripple_rad)
		ellipse.pos = (ripple_pos[0] - ripple_rad/2.,
		               ripple_pos[1] - ripple_rad/2.)

	def set_color(self, instance, value):
		self.col_instruction.rgba = value

	def on_touch_up(self, touch):
		if self.state == "down":
			self.finish_ripple()
		return super(RippleBehavior, self).on_touch_up(touch)

	def finish_ripple(self):
		rc = self.ripple_color
		anim = Animation(
			ripple_color=[rc[0], rc[1], rc[2], 0.],
			t=self.ripple_func_out, duration=self.ripple_duration_out)
		anim.bind(on_complete=self.anim_complete)
		anim.start(self)

	def anim_complete(self, anim, instance):
		self.ripple_rad = 10
		self.canvas.after.clear()