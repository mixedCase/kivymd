# -*- coding: utf-8 -*-
from kivymd.layouts import MaterialBoxLayout
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty


class SlidingModal(MaterialBoxLayout):
	"""ModalView that will slide in and out from a side"""

	side = StringProperty("right")
	"""Position where the widget will slide from.

	Valid values are "left", "right", "bottom" and "top".
	"""

	_status = "closed"
	_hidden_pos = (0, 0)
	_visible_pos = (0, 0)
	_anim_alpha = NumericProperty(0)
	_anim_duration = NumericProperty(.5)

	def __init__(self, **kwargs):
		self._window = Window
		super(SlidingModal, self).__init__(**kwargs)

	def on_size(self, instance, value):
		self._update_side(self.side)

	def on_side(self, instance, value):
		self._update_side(value)

	def _update_side(self, value):
		if value == "right":
			self._hidden_pos = (Window.width, 0)
			self._visible_pos = (Window.width - self.width, 0)
		elif value == "bottom":
			self._hidden_pos = (0, 0 - self.height)
			self._visible_pos = (0, 0)
		elif value == "top":
			self._hidden_pos = (0, Window.height)
			self._visible_pos = (0, Window.height - self.height)
		elif value == "left":
			self._hidden_pos = (0 - self.width, 0)
			self._visible_pos = (0, 0)
		else:
			raise ValueError("Valid values for side are \"left\", \"right\", "
			                 "\"bottom\" and \"top\"")

	def open(self, *largs):
		Window.add_widget(self)
		Window.bind(on_keyboard=self._handle_keyboard)
		self.pos = self._hidden_pos
		self._status = "open"
		Animation(pos=self._visible_pos,
		          t="in_out_expo",
		          d=self._anim_duration).start(self)
		Animation(_anim_alpha=.8, d=.2).start(self)

	def dismiss(self, *largs, **kwargs):
		self._status = "closed"
		a = Animation(pos=self._hidden_pos,
		              t="out_expo",
		              d=self._anim_duration)
		a.bind(on_complete=lambda *x: self._remove_widget())
		a.start(self)
		Animation(_anim_alpha=0., d=.2).start(self)

	def _remove_widget(self):
		Window.remove_widget(self)
		Window.unbind(on_keyboard=self._handle_keyboard)

	def _handle_keyboard(self, window, key, *largs):
		if key == 27:
			self.dismiss()
			return True

	def on_touch_down(self, touch):
		if not self.collide_point(*touch.pos):
			return True
		return super(SlidingModal, self).on_touch_down(touch)

	def on_touch_move(self, touch):
		if not self.collide_point(*touch.pos):
			return True
		return super(SlidingModal, self).on_touch_move(touch)

	def on_touch_up(self, touch):
		if not self.collide_point(*touch.pos):
			return True
		return super(SlidingModal, self).on_touch_up(touch)


class ExpandableSlidingModal(SlidingModal):
	_touch_pos = None
	min_height = NumericProperty()
	max_height = NumericProperty()

	def on_touch_down(self, touch):
		self._set_touch_down_attr(touch)
		return super(ExpandableSlidingModal, self).on_touch_down(touch)

	def _set_touch_down_attr(self, touch):
		self._touch_pos = touch.pos
		self._moved = False

	def on_touch_move(self, touch):
		self._moved = True
		if self.side == "bottom":
			new_height = self.height + (touch.pos[1] - self._touch_pos[1])
			self._touch_pos = touch.pos
			if self.resizing_condition(new_height):
				pass
			else:
				return
			if new_height < self.min_height:
				new_height = self.min_height
			elif new_height > self.max_height:
				new_height = Window.height
			self.height = new_height
		else:
			raise NotImplementedError("Only \"bottom\" implemented right now "
			                          "for ExpandableSlidingModal, sorry")
		return super(ExpandableSlidingModal, self).on_touch_move(touch)

	def resizing_condition(self, new_height):
		return True

	def on_touch_up(self, touch):
		self._touch_pos = None
		return super(ExpandableSlidingModal, self).on_touch_up(touch)
