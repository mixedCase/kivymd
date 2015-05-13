import kivymd
from kivy.clock import Clock
from kivy.core.image import Image
from kivy.properties import NumericProperty, BoundedNumericProperty
from kivy.graphics import Color, BorderImage
from kivy.animation import Animation
from kivy.metrics import dp, Metrics

class ElevationBehaviour(object):
	elevation_normal = BoundedNumericProperty(2, min=2, max=12)
	elevation_raised = BoundedNumericProperty(0, min=0, max=12)

	_elevation = NumericProperty()
	_soft_border = NumericProperty(8)
	_hard_border = NumericProperty(30) #26

	def __init__(self, **kwargs):
		self._elevation = self.elevation_normal
		self.ratio = Metrics.dpi / 100
		if self.elevation_raised == 0:
			self.elevation_raised = self.elevation_normal + 6
		self.texture_hard = Image('atlas://' + kivymd.images_path + 'el_shadows.atlas/h_shadow', mipmap=True).texture
		self.texture_soft = Image('atlas://' + kivymd.images_path + 'el_shadows.atlas/s_shadow', mipmap=True).texture
		self.elevation_press_anim = Animation(_elevation=self.elevation_raised, duration=.2, t='out_quad')
		self.elevation_release_anim = Animation(_elevation=self.elevation_normal, duration=.2, t='out_quad')
		super(ElevationBehaviour, self).__init__(**kwargs)

		with self.canvas.before:
			self._soft_col = Color(rgba=(1, 1, 1, .4))
			self.border_soft = BorderImage(texture=self.texture_soft)
			self._hard_col = Color(rgba=(1, 1, 1, .16))
			self.border_hard = BorderImage(texture=self.texture_hard)
			print Metrics.dpi_rounded

		self.bind(pos=self.update_shadow,
				  size=self.update_shadow,
				  _elevation=self.update_shadow)

		Clock.schedule_once(self.update_shadow, 0)

	def update_shadow(self, *args):
		if hasattr(self, 'disabled'):
			if not self.disabled:
					width = self.width + (self.ratio * 1.3**self._elevation) #(ratio * 1.3**self._elevation)
					height = self.height + (self.ratio * 1.3**self._elevation) #(ratio * 1.3**self._elevation)
					self._soft_col.a = .4 * .98**self._elevation
					self.border_soft.size=(width, height)
					self.border_soft.pos=(self.center_x - width / 2,
										  self.center_y - (height / 2) - (self.ratio * 1.2 ** self._elevation))
					self.border_soft.border = (self._soft_border * .9**self._elevation,
											   self._soft_border * .9**self._elevation,
											   self._soft_border * .9**self._elevation,
											   self._soft_border * .9**self._elevation)

					width = self.width + 14 #(ratio * 6)
					height = self.height + 14 #(ratio * 6)

					self._hard_col.a = .16 * .97**self._elevation

					self.border_hard.size = (width, height)
					self.border_hard.pos = (self.center_x - width / 2,
											self.center_y - (height / 2) - (self.ratio * 1 ** self._elevation))

					self.border_hard.border = (self._hard_border * .83**self._elevation,
											   self._hard_border * .83**self._elevation,
											   self._hard_border * .83**self._elevation,
											   self._hard_border * .83**self._elevation)
			else:
				self._soft_col.a = 0
				self._hard_col.a = 0

	def on_touch_down(self, touch):
		if hasattr(self, 'disabled'):
			if not self.disabled:
				if touch.is_mouse_scrolling:
					return False
				if not self.collide_point(touch.x, touch.y):
					return False
				if self in touch.ud:
					return False
				self.elevation_press_anim.stop(self)
				self.elevation_press_anim.start(self)

	def on_touch_up(self, touch):
		if hasattr(self, 'disabled'):
			if not self.disabled:
				self.elevation_release_anim.stop(self)
				self.elevation_release_anim.start(self)