# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.label import Label
from kivy.properties import DictProperty, BooleanProperty, OptionProperty, StringProperty, ListProperty
from kivy.metrics import sp
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from material_resources import get_icon_char
from layouts import BackgroundColorCapableWidget
from theme import ThemeBehaviour

class MaterialLabel(ThemeBehaviour, Label, BackgroundColorCapableWidget):
	""":class:`MaterialLabel(**kwargs)` uses by default the Roboto font. With 
	:attr:`font_style` and :attr:`color_style` you can choose from some pre-defined
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

	theme_color = OptionProperty('Primary', options=['Primary',
													 'Secondary',
													 'Hint',
													 'Error'])
	"""With :attr:`theme_color` you can choose from a list of pre-defined text colors.
	Look at the	documentation on :class:`~kivymd.theme.ThemeManager` for more information.

	Available styles:
		* 'Primary'
		* 'Secondary'
		* 'Hint'
		* 'Error'

	The :attr:`theme_color` is a
	:class:`kivy.properties.OptionProperty` and defaults to ``Primary``.
	"""

	color_style = OptionProperty(None, options=['Light', 'Dark'], allownone=True)
	"""Use :attr:`color_style` to override the default :class:`~kivymd.theme.ThemeManager.theme_style`.

	Available styles:
		* 'Light'
		* 'Dark'

	.. note:
		This will not have any effect if :attr:`auto_color` is True.

	The :attr:`color_style` is a
	:class:`kivy.properties.OptionProperty` and defaults to ``None``.
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
	_color_styles = DictProperty({'Primary':'primary_text_color',
								  'Secondary':'secondary_text_color',
								  'Hint':'hint_text_color',
								  'Error':'error_color'})

	def __init__(self, text='', font_style='Body1', theme_color='Primary', **kwargs):
		super(MaterialLabel, self).__init__(**kwargs)
		self.size_hint_x = None

		self.text = text
		self.font_style = font_style
		self.theme_color = theme_color
		# self.halign = 'left'
		# self.valign = 'middle'

		self.bind(size=self.update,
				  pos=self.update,
				  font_style=self.update,
				  theme_color=self.update,
				  text=self.update)

		Clock.schedule_once(self.update, 0)

	def update(self, *args):
		self.font_name = self._font_styles[self.font_style][0]
		self.bold = self._font_styles[self.font_style][1]
		self.font_size = sp(self._font_styles[self.font_style][2])

		if self.font_style == 'Button':
			self.halign = 'center'

		if self.font_style == 'Icon':
			self.text = u"{}".format(get_icon_char(self.icon))

		if self.auto_color:
			style = 'Light' if self.has_light_background else 'Dark'
		elif not self.color_style == None:
			style = self.color_style
		else:
			style = self._theme_cls.theme_style

		self.color = getattr(self._theme_cls, self._color_styles[self.theme_color])(style=style)

	def on_texture_size(self, *args):
		if self.texture_size[0] > self.width:
			self.width = self.texture_size[0]
		self.text_size = self.width, None