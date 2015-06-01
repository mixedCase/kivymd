import kivymd
from kivy.clock import Clock
from kivy.core.image import Image
from kivy.properties import NumericProperty, AliasProperty
from kivy.graphics import Color, BorderImage, Ellipse, StencilPush, StencilPop, StencilUse, \
	StencilUnUse, Rectangle
from kivy.metrics import Metrics

class ElevationBehaviour(object):
	"""Doesn't work with MaterialRelativeLayout
	"""

	_elevation = NumericProperty(0)
	def _get_elevation(self):
		return self._elevation

	def _set_elevation(self, elevation):
		try:
			self._elevation = int(elevation)
			Clock.schedule_once(self.update_shadow, 0)
		except:
			self._elevation = 0

	elevation = AliasProperty(_get_elevation, _set_elevation, bind=('_elevation', ))
	"""Get or set the elevation of the widget. Elevation must be in the range of 0-12.
	If an invalid argument is passed when trying to set the :attr:`elevation` it will
	fall back to default, 0.

	The :attr:`elevation` is a
	:class:`kivy.properties.AliasProperty` and defaults to ``0``.
	"""

	_soft_border = NumericProperty(8)
	_hard_border = NumericProperty(30)

	def __init__(self, **kwargs):
		self.ratio = Metrics.dpi / 100

		self.texture_hard = Image('atlas://' + kivymd.images_path + 'el_shadows.atlas/h_shadow', mipmap=True).texture
		self.texture_soft = Image('atlas://' + kivymd.images_path + 'el_shadows.atlas/s_shadow', mipmap=True).texture
		super(ElevationBehaviour, self).__init__(**kwargs)

		with self.canvas.before:
			self._soft_col = Color(rgba=(1, 1, 1, .4))
			self.border_soft = BorderImage(texture=self.texture_soft)
			self._hard_col = Color(rgba=(1, 1, 1, .16))
			self.border_hard = BorderImage(texture=self.texture_hard)

		self.bind(pos=self.update_shadow,
				  size=self.update_shadow,
				  elevation=self.update_shadow)

		Clock.schedule_once(self.update_shadow, 0)

	def update_shadow(self, *args):
		if self._elevation == 0:
			self._hard_col.a = 0
			self._soft_col.a = 0
		else:
			width = self.width + (self.ratio * 1.3**self._elevation)
			height = self.height + (self.ratio * 1.3**self._elevation)

			self._soft_col.a = .4 * .98**self._elevation
			self.border_soft.size=(width, height)

			self.border_soft.pos=(self.center_x - width / 2,
								  self.center_y - (height / 2) - (self.ratio * 1.2 ** self._elevation))
			self.border_soft.border = (self._soft_border * .9**self._elevation,
									   self._soft_border * .9**self._elevation,
									   self._soft_border * .9**self._elevation,
									   self._soft_border * .9**self._elevation)

			width = self.width + 14
			height = self.height + 14

			self._hard_col.a = .16 * .97**self._elevation

			self.border_hard.size = (width, height)

			self.border_hard.pos = (self.center_x - width / 2,
									self.center_y - (height / 2) - (self.ratio * 1 ** self._elevation))

			self.border_hard.border = (self._hard_border * .83**self._elevation,
									   self._hard_border * .83**self._elevation,
									   self._hard_border * .83**self._elevation,
									   self._hard_border * .83**self._elevation)

class CircularElevationBehaviour(object):

	_elevation = NumericProperty(0)
	def _get_elevation(self):
		return self._elevation

	def _set_elevation(self, elevation):
		try:
			self._elevation = int(elevation)
			Clock.schedule_once(self.update_shadow, 0)
		except:
			self._elevation = 0

	elevation = AliasProperty(_get_elevation, _set_elevation, bind=('_elevation', ))
	"""Get or set the elevation of the widget. Elevation must be in the range of 0-12.
	If an invalid argument is passed when trying to set the :attr:`elevation` it will
	fall back to default, 0.

	The :attr:`elevation` is a
	:class:`kivy.properties.AliasProperty` and defaults to ``0``.
	"""

	_soft_border = NumericProperty(8)
	_hard_border = NumericProperty(30)

	def __init__(self, **kwargs):
		self.ratio = Metrics.dpi / 100

		self.texture_hard = Image('atlas://' + kivymd.images_path + 'el_c_shadows.atlas/h_shadow', mipmap=True).texture
		self.texture_soft = Image('atlas://' + kivymd.images_path + 'el_c:shadows.atlas/s_shadow', mipmap=True).texture
		super(ElevationBehaviour, self).__init__(**kwargs)
		self.b_soft = BorderImage(texture=self.texture_soft)
		self.b_hard = BorderImage(texture=self.texture_hard)

		with self.canvas.before:
			# StencilPush()
			# Ellipse(size=self.size,
			# 		pos=self.pos)
			# StencilUse()
			self._soft_col = Color(rgba=(1, 1, 1, .4))
			self.border_soft = Ellipse(texture=self.b_soft.texture)
			self._hard_col = Color(rgba=(1, 1, 1, .16))
			self.border_hard = Ellipse(texture=self.b_hard.texture)
			# StencilUnUse()
			#
			# StencilPop()

		self.bind(pos=self.update_shadow,
				  size=self.update_shadow,
				  elevation=self.update_shadow)

		Clock.schedule_once(self.update_shadow, 0)

	def update_shadow(self, *args):
		if self._elevation == 0:
			self._hard_col.a = 0
			self._soft_col.a = 0
		else:
			width = self.width + (self.ratio * 1.3**self._elevation)
			height = self.height + (self.ratio * 1.3**self._elevation)

			self._soft_col.a = .4 * .98**self._elevation
			self.border_soft.size=(width, height)

			self.border_soft.pos=(self.center_x - width / 2,
								  self.center_y - (height / 2) - (self.ratio * 1.2 ** self._elevation))
			self.b_soft.border = (self._soft_border * .9**self._elevation,
									   self._soft_border * .9**self._elevation,
									   self._soft_border * .9**self._elevation,
									   self._soft_border * .9**self._elevation)

			width = self.width + 14
			height = self.height + 14

			self._hard_col.a = .16 * .97**self._elevation

			self.border_hard.size = (width, height)

			self.border_hard.pos = (self.center_x - width / 2,
									self.center_y - (height / 2) - (self.ratio * 1 ** self._elevation))

			self.b_hard.border = (self._hard_border * .83**self._elevation,
									   self._hard_border * .83**self._elevation,
									   self._hard_border * .83**self._elevation,
									   self._hard_border * .83**self._elevation)