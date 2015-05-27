# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.label import Label
from kivy.properties import DictProperty, BooleanProperty, OptionProperty, StringProperty, ListProperty
from kivy.metrics import sp, dp
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from material_resources import get_icon_char, get_rgba_color
from layouts import BackgroundColorCapableWidget
from theme import ThemeBehaviour

class MaterialLabel(ThemeBehaviour, Label, BackgroundColorCapableWidget):
	""":class:`MaterialLabel(**kwargs)` uses by default the Roboto font. With 
	:attr:`font_style` and :attr:`theme_style` you can choose from some pre-defined
	styles that's described in the Material Design guide lines.
	 
	The :class:`MaterialLabel` is a sub-class of
	:class:`kivymd.theme.ThemeBehaviour`, :class:`kivy.uix.Label`
	and :class:`kivymd.layouts.BackgroundColorCapableWidget`.
	"""

	font_style = OptionProperty('Body1', options=['Body1', 'Body2', 'Caption', 'Subhead', 'Title',
												  'Headline', 'Display1', 'Display2', 'Display3',
												  'Display4', 'Button', 'Icon'])
	"""With :attr:`font_style` you can choose from a list of pre-defined font styles:

	Available styles:
		* 'Body1'		- Roboto Regular,				14sp
		* 'Body2'		- Roboto Medium,				14sp
		* 'Caption'		- Roboto Regular,				12sp
		* 'Subhead'		- Roboto Regular,				16sp
		* 'Title'		- Roboto Medium,				20sp
		* 'Headline'	- Roboto Regular,				24sp
		* 'Display1'	- Roboto Regular,				34sp
		* 'Display2'	- Roboto Regular,				45sp
		* 'Display3'	- Roboto Regular,				56sp
		* 'Display4'	- Roboto Light',				112sp
		* 'Button'		- Roboto Medium,				14sp
		* 'Icon'		- Material Design Iconic Font,	24sp

	.. note:
		For information on available icons, go to
		http://zavoloklom.github.io/material-design-iconic-font/

	.. note:
		'Button' will automatically make the text to upper case.

	The :attr:`font_style` is a
	:class:`kivy.properties.OptionProperty` and defaults to ``Body1``.
	"""

	theme_text_color = OptionProperty('Primary', options=['Primary',
														  'Secondary',
														  'Hint',
														  'Error'])
	"""With :attr:`theme_text_color` you can choose from a list of pre-defined text colors.
	Look at the	documentation on :class:`~kivymd.theme.ThemeManager` for more information.

	Available styles:
		* 'Primary'
		* 'Secondary'
		* 'Hint'
		* 'Error'

	The :attr:`theme_text_color` is a
	:class:`kivy.properties.OptionProperty` and defaults to ``Primary``.
	"""

	theme_style = OptionProperty(None, options=['Light', 'Dark', 'Custom'], allownone=True)
	"""Use :attr:`theme_style` to override the default :class:`~kivymd.theme.ThemeManager.theme_style`.

	Available styles:
		* 'Light'
		* 'Dark'
		* 'Custom'

	To give the text a custom color, set :attr:`theme_style` to 'Custom'::

		#Create a label
		label = MaterialLabel(theme_style='Custom', text="Testing a label")

		#Give the text a custom color by using...
		label.text_color = (.5, .7, .4, 1.)

		#Or by giving it a color tuple from the theme palettes...
		label.text_color = ['Green', '500']


	The :attr:`theme_style` is a
	:class:`kivy.properties.OptionProperty` and defaults to ``None``.
	"""

	text_color = ListProperty(None, allownone=True)
	"""Use :attr:`text_color` in combination with :attr:`theme_style` set to 'Custom' to give
	the text a custom color.

	You can pass the color as rgba or as a theme palette tuple, eg ['Green', '500']

	The :attr:`text_color` is a
	:class:`kivy.properties.ListProperty` and defaults to ``None``.
	"""

	icon = StringProperty('md-android')
	"""If :class:`MaterialLabel.font_style` is set to 'Icon', use :attr:`icon` to set
	the icon. For a list of available icons, go to::

		http://zavoloklom.github.io/material-design-iconic-font

	.. note::
		This property has no effect if not :attr:`font_style` is set to 'Icon'.

	The :attr:`icon` is a
	:class:`kivy.properties.StringProperty` and defaults to ``md-android``.
	"""

	_font_styles = DictProperty({'Body1':['Roboto', False, 14],
								 'Body2':['Roboto', True, 14],
								 'Caption':['Roboto', False, 12],
								 'Subhead':['Roboto', False, 16],
								 'Title':['Roboto', True, 20],
								 'Headline':['Roboto', False, 24],
								 'Display1':['Roboto', False, 34],
								 'Display2':['Roboto', False, 45],
								 'Display3':['Roboto', False, 56],
								 'Display4':['RobotoLight', False, 112],
								 'Button':['Roboto', True, 14],
								 'Icon':['Icons', False, 24]})

	def __init__(self, **kwargs):
		super(MaterialLabel, self).__init__(**kwargs)
		self.text_size = self.size
		self.bind(theme_text_color=self._update_color,
				  theme_style=self._update_color,
				  text_color=self._update_color,
				  size=self._fix_size)
		self.disabled_color = self._theme_cls.disabled_text_color()
		Clock.schedule_once(self._update_color, 0)

	def on_font_style(self, instance, style):
		self.font_style = style

		if self.font_style == 'Button':
			self.halign = 'center'
			self.valign = 'middle'

		if self.font_style == 'Icon':
			self.text = u"{}".format(get_icon_char(self.icon))

		self.font_name = self._font_styles[self.font_style][0]
		self.bold = self._font_styles[self.font_style][1]
		self.font_size = sp(self._font_styles[self.font_style][2])

	def on_icon(self, instance, icon):
		if self.font_style == 'Icon':
			self.text = u"{}".format(get_icon_char(self.icon))

	def _update_color(self, *args):
		if self.theme_style:
			style = self.theme_style
		else:
			style = self._theme_cls.theme_style

		if style == 'Custom':
			if len(self.text_color) == 2:
				self.color = get_rgba_color(self.text_color)
				return
			if len(self.text_color) == 4:
				self.color = self.text_color
				return
			else:
				self.color = (1, 1, 1, 1)
				return
		else:
			self.color = self._get_color(style)

	def _get_color(self, style):
			if self.theme_text_color == 'Primary':
				return self._theme_cls.primary_text_color(style=style)
			elif self.theme_text_color == 'Secondary':
				return self._theme_cls.secondary_text_color(style=style)
			elif self.theme_text_color == 'Hint':
				return self._theme_cls.hint_text_color(style=style)
			elif self.theme_text_color == 'Error':
				return self._theme_cls.error_color

	def _fix_size(self, widget, size):
		self.text_size = size[0], None
		self.texture_update()
		if self.size_hint_y == None and self.size_hint_x != None:
			self.height = max(self.texture_size[1], self.line_height)
		elif self.size_hint_x == None and self.size_hint_y != None:
			self.width = self.texture_size[0]
