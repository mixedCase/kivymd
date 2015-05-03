# -*- coding: utf-8 -*-
from threading import Timer as ThreadedTimer

from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.animation import Animation
from kivy.metrics import dp

from kivymd import helpers
from layouts import MaterialRelativeLayout
from kivymd.shadow import Shadow


class SlidingPanel(MaterialRelativeLayout):
	"""An empty panel that slides from a side"""

	side = StringProperty("left")
	"""Side from which the menu will slide from

	Valid values are "left" and "right"
	"""

	has_shadow = BooleanProperty(True)
	"""Selects wether or not to show shadow behind panel"""

	animation_length = NumericProperty(0.3)
	"""How long will the animation last"""

	def __init__(self, width=dp(200), **kwargs):
		self.animation_open = Animation(duration=self.animation_length,
		                                t="out_sine")
		self.animation_dismiss = Animation(duration=self.animation_length,
		                                   t="out_sine")

		self.shadow = Shadow(width=0, opacity=0.8, size_hint_x=None,
		                     on_release=lambda x: self.dismiss())
		super(SlidingPanel, self).__init__(**kwargs)
		self.orientation = "vertical"
		self.width = width
		self.size_hint = (None, None)
		self.status = "closed"
		self.timer = None

		self.shadow.fade_out(0)
		self.bind(height=self.shadow.setter('height'))
		helpers.bind_to_rotation(self._device_rotated)

	def on_touch_down(self, touch):
		# Prevents touch events from propagating to anything below the widget.
		super(SlidingPanel, self).on_touch_down(touch)
		if self.collide_point(*touch.pos):
			return True

	def open(self):
		if self.status != "closed":
			return
		self.update_animations()
		if self.has_shadow:
			self.shadow.fade_in(self.animation_length, add_to=self)
		self.animation_open.start(self)
		self.status = "opening"
		self.timer = ThreadedTimer(
			self.animation_length + 0.1, self._fix_status).start()

	def dismiss(self):
		if self.status != "open":
			return
		self.update_animations()
		if self.has_shadow:
			self.shadow.fade_out(self.animation_length, remove_from=self)
		self.animation_dismiss.start(self)
		self.status = "closing"
		self.timer = ThreadedTimer(
			self.animation_length + 0.1, self._fix_status).start()

	def update_animations(self):
		if self.side == "left":
			self.shadow.x = self.width
			if self.status == "closed":
				self.animation_open.animated_properties['x'] = self.x +\
			                                                   self.width
			elif self.status == "open":
				self.animation_dismiss.animated_properties['x'] = self.x -\
				                                                  self.width
		elif self.side == "right":
			self.shadow.x = 0 - self.shadow.width
			if self.status == "closed":
				self.animation_open.animated_properties['x'] = \
					self.parent.width - self.width
			elif self.status == "open":
				self.animation_dismiss.animated_properties['x'] = \
					self.parent.x + self.width
		self.animation_dismiss.animated_properties['y'] = float(self.y)

	def _device_rotated(self, orientation):
		self.update_animations()

	def toggle(self):
		if self.status == "open":
			self.dismiss()
		elif self.status == "closed":
			self.open()

	def _fix_status(self):
		if self.status == "opening":
			self.status = "open"
		elif self.status == "closing":
			self.status = "closed"
		else:
			return
		self.timer = None

	def on_side(self, instance, value):
		if value == "left":
			self.shadow.x = self.width
			value.unbind(width=self.setter('x'))
		elif value == "right":
			self.shadow.x = self.shadow.width - self.width
		else:
			raise ValueError(
				"Valid values for side are \"left\" and \"right\"")

	def on_parent(self, instance, value):
		value.bind(height=self.setter('height'))
		value.bind(x=self._set_x)
		value.bind(y=self._set_y)
		value.bind(width=self.shadow.setter('width'))
		if self.side == "left":
			self.x = value.x - self.width
		elif self.side == "right":
			value.bind(width=self.setter('x'))

	def _set_x(self, instance, value):
		if self.side == "left":
			self.x = value - self.width
		elif self.side == "right":
			self.x = instance.width

	def _set_y(self, instance, value):
		self.y = value
