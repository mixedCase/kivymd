# -*- coding: utf-8 -*-
__version__ = "0.0.1"

from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.widget import Widget
from kivy.properties import (StringProperty, OptionProperty, AliasProperty,
							 ObjectProperty, BooleanProperty)
from kivymd.material_resources import get_rgba_color, FONTS, is_light_color


class ThemeManager(Widget):
	"""The :class:`ThemeManager()` manage the overall appearance by implementing the Material
	Design style guidelines for colors and fonts.

	.. note::
		This is a work in progress and not a complete implementation of all the parts of
		the official Material Design.

	To use the Theme Manager, add a :attr:`theme_cls` to your :class:`kivy.app.App()` instance::

		from kivymd.theme import ThemeManager

		theme_cls = ThemeManager()


	**Theme style**

	The Material theme comes in two styles, ``Light`` and ``Dark``. This setting defines the
	background color of the app::

		# Set the overall theme style by choosing between ``Light`` or ``Dark``
		self.theme_cls.theme_style = 'Dark'

	This will determine the background colors and text colors:

		:attr:`main_background_color` - This is the main background color for the app.

		.. note::
			* Light: :attr:`main_background_color` = Grey 200
			* Dark: :attr:`main_background_color` = #303030


		:attr:`dialog_background_color` - This is the background color used by
		:class:`MaterialDialog()` and :class:`MaterialCard`.

		.. note::
			* Light: :attr:`dialog_background_color` = Grey 50
			* Dark: :attr:`dialog_background_color` = Grey 800



	**Theme colors**

	The rest of the user interface uses colors from a pre-defined set of colors organized
	in ``palettes``. The :class:`ThemeManager()` handles two palettes, one for the primary colors
	and one for the accent colors::

		# Set the primary color palette
		self.theme_cls.primary_palette = 'Blue'

	These color palettes comprises primary and accent colors that can be used for illustration or
	to develop your brand colors. They’ve been designed to work harmoniously with each other.

	Each palette is divided into 10 primary colors ('50', '100' ... '900') and 4 accent
	colors ('A100', 'A200', 'A400' and 'A700). These colors are different hues of the main color
	and are combined in a specific manner in order to keep the theme consistent:

		* :attr:`primary_color` is by default the 500 hue of the primary color palette

		* :attr:`primary_dark` is by default the 700 hue of the primary color palette

		* :attr:`primary_light` is by default the 100 hue of the primary color palette

	.. warning::
		The palettes ``Brown``, ``Grey`` and ``BlueGrey`` doesn't have any accent colors.

	It's recommended not to use more than three different hues of the primary color. However, the
	default hues can be customized::

		# Set the primary color hue to '400'
		self.theme_cls.primary_hue = '400'

		# Set the primary dark hue to '900'
		self.theme_cls.primary_dark_hue = '900'

		# Set the primary light hue to '200'
		self.theme_cls.primary_light_hue = '200'

	The :attr:`accent_palette` is used to set the accent color in the app::

		# Set the accent color to 'Red'
		self.theme_cls.accent_palette = 'Red'

	The :attr:`accent_color` should be used for primary action buttons and components
	like switches or sliders. The main accent color uses the ``A200`` hue but if
	the background is too light or dark there are two fallback colors that can
	be used instead:

		* :attr:`accent_dark` is by default the ``A400`` hue of the accent color

		* :attr:`accent_light` is by default the ``A100`` hue of the accent color

	These default accent color hues can also be customized::

		# Set the accent color main hue to 'A400'
		self.theme_cls.accent_hue = 'A400'

		# Set the darker fallback accent color to 'A700'
		self.theme_cls.accent_dark_hue = 'A700'



	**Fonts and Text color**


	The Kivy Material Design theme uses Roboto as the default font and Material
	Design Iconic font for icons. When an instance of :class:`ThemeManager()` is
	initialized these fonts are registered with :class:`kivy.core.text.LabelBase()`.

	.. note:
		For more information on the amazing Material Design Iconic Font, go to
		http://zavoloklom.github.io/material-design-iconic-font/

	The color of the text within the app is determined primarily by the :attr:`theme_style`.
	Different text blocks should be separated by their importance relative to other text:

		:attr:`primary_text_color` - This is the primary color for text blocks.

		.. note::
			* Light: :attr:`primary_text_color` = 87% black
			* Dark: :attr:`primary_text_color` = 100% white


		:attr:`secondary_text_color` - This is the secondary color that should be used for
		text that's not as important as other text.

		.. note::
			* Light: :attr:`secondary_text_color` = 54% black
			* Dark: :attr:`secondary_text_color` = 70% white


		:attr:`hint_text_color` - This is the color used for hint text by :class:`MaterialTextInput()`.

		.. note::
			* Light: :attr:`hint_text_color` = 26% black
			* Dark: :attr:`hint_text_color` = 30% white


		:attr:`disabled_color` is the same color as :attr:`hint_text_color` and should be used for
		disabled widgets such as :class:`MaterialFlatButton()`.


		:attr:`divider_color` - This is the color used by :class:`Divider()`.

		.. note::
			* Light: :attr:`hint_text_color` = 12% black
			* Dark: :attr:`hint_text_color` = 12% white

	"""

	theme_style = OptionProperty('Light', options=['Light', 'Dark'])
	"""Set the overall color scheme.

	Determines the :attr:`main_background_color` and :attr:`dialog_background_color`.

	Available styles:
		* 'Light'
		* 'Dark'

	The :attr:`theme_style` is a
	:class:`kivy.properties.OptionProperty` and defaults to ``Light``.
	"""

	def _get_main_background_color(self):
		return get_rgba_color([self.theme_style, 'MainBackground'])

	main_background_color = AliasProperty(_get_main_background_color, bind=('theme_style', ))
	"""**(Read only)** :attr:`main_background_color` holds the main background color.

	This is a attribute that's determined by the :attr:`theme_style`:

	* :attr:`theme_style('Light')` sets the :attr:`main_background_color` to ``Grey 200`` (in rgb)
	* :attr:`theme_style('Dark')` sets the :attr:`main_background_color` ``(0.188, 0.188, 0.188)``

	The :attr:`main_background_color` is a
	:class:`kivy.properties.AliasProperty` and defaults to ``Grey 200`` in rgb.
	"""

	def _get_dialog_background_color(self):
		return get_rgba_color([self.theme_style, 'DialogBackground'])

	dialog_background_color = AliasProperty(_get_dialog_background_color, bind=('theme_style', ))
	"""**(Read only)** :attr:`dialog_background_color` holds the background color used
	by :class:`MaterialDialog()` and :class:`MaterialCard()`.

	This is a attribute that's determined by the :attr:`theme_style`:

	* :class:`ThemeManager.theme_style('Light')` sets the :attr:`dialog_background_color` to ``Grey 50`` (in rgb)
	* :class:`ThemeManager.theme_style('Dark')` sets the :attr:`dialog_background_color` to ``Grey 800`` (in rgb)


	The :attr:`main_background_color` is a
	:class:`kivy.properties.AliasProperty` and defaults to ``Grey 200`` in rgb.
	"""

	primary_palette = OptionProperty('Grey',
									 options=['Pink', 'Blue', 'Indigo', 'BlueGrey', 'Brown', 'LightBlue', 'Purple',
											  'Grey', 'Yellow', 'LightGreen', 'DeepOrange', 'Green', 'Red', 'Teal',
											  'Orange', 'Cyan', 'Amber', 'DeepPurple', 'Lime'])
	"""The primary color palette.

	Available palettes:
		* 'Pink'
		* 'Blue'
		* 'Indigo'
		* 'BlueGrey'
		* 'Brown'
		* 'LightBlue'
		* 'Purple'
		* 'Grey'
		* 'Yellow'
		* 'LightGreen'
		* 'DeepOrange'
		* 'Green'
		* 'Red'
		* 'Teal'
		* 'Orange'
		* 'Cyan'
		* 'Amber'
		* 'DeepPurple'
		* 'Lime'

	A Material Design theme is by default limited to three hues of the :attr:`primary_palette`:

	* ``500`` - the default hue that will be used for the :class:kivymd.`Toolbar` and should be used for other larger color blocks.

	* ``700`` - a darker hue.

	* ``100`` - a lighter hue.

	.. note::
		The :attr:`primary_hue`, :attr:`primary_dark_hue` and :attr:`primary_light_hue` can be
		customized by setting a different hue for the individual attributes.

	:class:`ThemeManager.primary_color` holds the primary color of the currently selected primary palette (in rgb).

	:class:`ThemeManager.primary_dark` holds the dark hue of the currently selected primary palette (in rgb).

	:class:`ThemeManager.primary_light` holds the light hue of the currently selected primary palette (in rgb).

	The :attr:`primary_palette` is a
	:class:`kivy.properties.OptionProperty` and defaults to ``Grey``.
	"""

	primary_hue = OptionProperty('500', options=['50', '100', '200', '300', '400', '500', '600', '700', '800',
												 '900', 'A100', 'A200', 'A400', 'A700'])
	"""The :attr:`primary_hue` holds the default hue for the primary color palette.

	Available hues:
		* '50'
		* '100'
		* '200'
		* '300'
		* '400'
		* '500'
		* '600'
		* '700'
		* '800'
		* '900'
		* 'A100' **(not in palettes ``Brown``, ``Grey`` and ``BlueGrey``)**
		* 'A200' **(not in palettes ``Brown``, ``Grey`` and ``BlueGrey``)**
		* 'A400' **(not in palettes ``Brown``, ``Grey`` and ``BlueGrey``)**
		* 'A700' **(not in palettes ``Brown``, ``Grey`` and ``BlueGrey``)**

	The :attr:`primary_hue` is a
	:class:`kivy.properties.OptionProperty` and defaults to ``500``.
	"""

	primary_dark_hue = OptionProperty('700', options=['50', '100', '200', '300', '400', '500', '600', '700', '800',
													  '900', 'A100', 'A200', 'A400', 'A700'])
	"""The :attr:`primary_dark_hue` holds the darker hue for the primary color palette.

	Available hues:
		* See documentation on :attr:`primary_hue`

	The :attr:`primary_dark_hue` is a
	:class:`kivy.properties.OptionProperty` and defaults to '700'.
	"""

	primary_light_hue = OptionProperty('100', options=['50', '100', '200', '300', '400', '500', '600', '700', '800',
													   '900', 'A100', 'A200', 'A400', 'A700'])
	"""The :attr:`primary_light_hue` holds the darker hue for the primary color palette.

	Available hues:
		* See documentation on :attr:`primary_hue`

	The :attr:`primary_light_hue` is a
	:class:`kivy.properties.OptionProperty` and defaults to ``100``.
	"""

	def _get_primary_color(self):
		return get_rgba_color([self.primary_palette, self.primary_hue])

	primary_color = AliasProperty(_get_primary_color, bind=('primary_palette', 'primary_hue', ))
	"""**(Read only)** :attr:`primary_color` holds the primary 500 hue of the currently selected
	:attr:`primary_palette` in rgb.

	The :attr:`primary_color` is a
	:class:`kivy.properties.AliasProperty` and defaults to 'Grey 500' in rgb format.
	"""

	def _get_primary_dark(self):
		return get_rgba_color([self.primary_palette, self.primary_dark_hue])

	primary_dark = AliasProperty(_get_primary_dark, bind=('primary_palette', 'primary_dark_hue'))
	"""**(Read only)** :attr:`primary_dark` holds the darker 700 hue of the currently selected
	:attr:`primary_palette` in rgb.

	The :attr:`primary_dark` is a
	:class:`kivy.properties.AliasProperty` and defaults to 'Grey 700' in rgb format.
	"""

	def _get_primary_light(self):
		return get_rgba_color([self.primary_palette, self.primary_light_hue])

	primary_light = AliasProperty(_get_primary_light, bind=('primary_palette', 'primary_light_hue', ))
	"""**(Read only)** :attr:`primary_light` holds the lighter 100 hue of the currently selected
	:attr:`primary_palette` in rgb.

	The :attr:`primary_light` is a
	:class:`kivy.properties.AliasProperty` and defaults to 'Grey 100' in rgb format.
	"""

	accent_palette = OptionProperty('Teal',
									options=['Pink', 'Blue', 'Indigo', 'BlueGrey', 'Brown', 'LightBlue', 'Purple',
											 'Grey', 'Yellow', 'LightGreen', 'DeepOrange', 'Green', 'Red', 'Teal',
											 'Orange', 'Cyan', 'Amber', 'DeepPurple', 'Lime'])
	"""The accent color palette.

	Available accent palettes:
		* 'Pink'
		* 'Blue'
		* 'Indigo'
		* 'LightBlue'
		* 'Purple'
		* 'Yellow'
		* 'LightGreen'
		* 'DeepOrange'
		* 'Green'
		* 'Red'
		* 'Teal'
		* 'Orange'
		* 'Cyan'
		* 'Amber'
		* 'DeepPurple'
		* 'Lime'

	Use the accent color for your primary action button and components like switches or sliders.

	.. note::
		If your accent color is too light or dark for the background color, choose
		:attr:`accent_light` or :attr:`accent_dark` as a fallback for these cases.

	:class:`ThemeManager.accent_color` holds the currently selected ``A200`` accent color (in rgb).

	:class:`ThemeManager.accent_light` holds the lighter ``A100`` hue of the currently selected accent color (in rgb).

	:class:`ThemeManager.accent_dark` holds the darker ``A400`` fallback hue of the currently selected accent color (in rgb).

	.. note::
		The :attr:`accent_color`, :attr:`accent_light` and :attr:`accent_dark` can be
		customized by setting a different hue for the individual attributes.

	The :attr:`accent_palette` is a
	:class:`kivy.properties.OptionProperty` and defaults to ``Teal``.
	"""

	accent_hue = OptionProperty('A200', options=['50', '100', '200', '300', '400', '500', '600', '700', '800',
												 '900', 'A100', 'A200', 'A400', 'A700'])
	"""The :attr:`accent_hue` holds the default hue for the accent color palette.

	Available hues:
		* See documentation on :attr:`primary_hue`

	The :attr:`accent_hue` is a
	:class:`kivy.properties.OptionProperty` and defaults to ``A200``.
	"""

	accent_light_hue = OptionProperty('A100', options=['50', '100', '200', '300', '400', '500', '600', '700', '800',
													   '900', 'A100', 'A200', 'A400', 'A700'])
	"""The :attr:`accent_light_hue` holds the lighter fallback hue for the accent color palette.

	Available hues:
		* See documentation on :attr:`primary_hue`

	The :attr:`accent_light_hue` is a
	:class:`kivy.properties.OptionProperty` and defaults to ``A100``.
	"""

	accent_dark_hue = OptionProperty('A400', options=['50', '100', '200', '300', '400', '500', '600', '700', '800',
													  '900', 'A100', 'A200', 'A400', 'A700'])
	"""The :attr:`accent_dark_hue` holds the darker fallback hue for the accent color palette.

	Available hues:
		* See documentation on :attr:`primary_hue`

	The :attr:`accent_dark_hue` is a
	:class:`kivy.properties.OptionProperty` and defaults to ``A400``.
	"""

	def _get_accent_color(self):
		return get_rgba_color([self.accent_palette, self.accent_hue])

	accent_color = AliasProperty(_get_accent_color, bind=('accent_palette', 'accent_hue', ))
	"""**(Read only)** :attr:`accent_color` holds the ``A200`` hue of the currently selected :attr:`accent_palette` in rgb.

	The :attr:`accent_color` is a
	:class:`kivy.properties.AliasProperty` and defaults to ``Teal A200`` in rgb format.
	"""

	def _get_accent_light(self):
		return get_rgba_color([self.accent_palette, self.accent_light_hue])

	accent_light = AliasProperty(_get_accent_light, bind=('accent_palette', 'accent_light_hue', ))
	"""**(Read only)** :attr:`accent_light` holds the lighter ``A100`` hue of the currently selected :attr:`accent_palette` in rgb.

	The :attr:`accent_light` is a
	:class:`kivy.properties.AliasProperty` and defaults to ``Teal A100`` in rgb format.
	"""

	def _get_accent_dark(self):
		return get_rgba_color([self.accent_palette, self.accent_dark_hue])

	accent_dark = AliasProperty(_get_accent_dark, bind=('accent_palette', 'accent_dark_hue', ))
	"""**(Read only)** :attr:`accent_dark` holds the darker ``A400`` hue of the currently selected :attr:`accent_palette` in rgb.

	The :attr:`accent_dark` is a
	:class:`kivy.properties.AliasProperty` and defaults to ``Teal A400`` in rgb format.
	"""

	def primary_text_color(self, style=None):
		if style == None:
			style = self.theme_style
		if style == 'Light':
			return get_rgba_color(['Dark', 'Black'], control_alpha=0.87)
		if style == 'Dark':
			return get_rgba_color(['Light', 'White'], control_alpha=1.0)

		return get_rgba_color(['Dark', 'Black'], control_alpha=0.87)
	"""**(Read only)** :attr:`primary_text_color(style=None)` returns the primary text color.

	This is by default determined by the :attr:`theme_style`:

	* :class:`ThemeManager.theme_style('Light')` sets the :attr:`primary_text_color` to 87% black (in rgb)
	* :class:`ThemeManager.theme_style('Dark')` sets the :attr:`primary_text_color` to 100% white (in rgb)

	You can however choose the desired style by passing it as an argument.
	"""

	def secondary_text_color(self, style=None):
		if style == None:
			style = self.theme_style
		if style == 'Light':
			return get_rgba_color(['Dark', 'Black'], control_alpha=0.54)
		if style == 'Dark':
			return get_rgba_color(['Light', 'White'], control_alpha=0.70)
		return get_rgba_color(['Dark', 'Black'], control_alpha=0.54)
	"""**(Read only)** :attr:`secondary_text_color` returns the secondary text color.

	This is by default determined by the :attr:`theme_style`:

	* :class:`ThemeManager.theme_style('Light')` sets the :attr:`secondary_text_color` to 54% black (in rgb)
	* :class:`ThemeManager.theme_style('Dark')` sets the :attr:`secondary_text_color` to 70% white (in rgb)

	You can however choose the desired style by passing it as an argument.
	"""

	def _get_hint_text_color(self, style=None):
		if style == None:
			style = self.theme_style
		if self.theme_style == 'Light':
			return get_rgba_color(['Dark', 'Black'], control_alpha=0.54)
		if self.theme_style == 'Dark':
			return get_rgba_color(['Light', 'White'], control_alpha=0.70)
		return get_rgba_color(['Dark', 'Black'], control_alpha=0.54)

	hint_text_color = AliasProperty(_get_hint_text_color, bind=None)
	"""**(Read only)** :attr:`hint_text_color` returns the hint text color.

	This is by default determined by the :attr:`theme_style`:

	* :class:`ThemeManager.theme_style('Light')` sets the :attr:`hint_text_color` to 26% black (in rgb)
	* :class:`ThemeManager.theme_style('Dark')` sets the :attr:`hint_text_color` to 30% white (in rgb)

	You can however choose the desired style by passing it as an argument.
	"""

	disabled_color = AliasProperty(_get_hint_text_color, bind=None)
	"""The :attr:`disabled_color` is the same as :attr:`hint_text_color` and is only there to make things more clear.

	"""

	def _get_divider_color(self):
		if self.theme_style == 'Light':
			return get_rgba_color(['Dark', 'Black'], control_alpha=0.12)
		if self.theme_style == 'Dark':
			return get_rgba_color(['Light', 'White'], control_alpha=0.12)

	divider_color = AliasProperty(_get_divider_color, bind=('theme_style', ))
	"""**(Read only)** :attr:`divider_color` holds the divider color. This is determined by the
	:attr:`theme_style`:

	* :class:`ThemeManager.theme_style('Light')` sets the :attr:`divider_color` to 12% black (in rgb)
	* :class:`ThemeManager.theme_style('Dark')` sets the :attr:`divider_color` to 12% white (in rgb)

	The :attr:`divider_color` is a
	:class:`kivy.properties.AliasProperty` and defaults to 12% black in rgb.
	"""

	_error_color = StringProperty('Red')
	_error_weight = StringProperty('A700')

	def _get_error_color(self):
		return get_rgba_color([self._error_color, self._error_weight])

	def _set_error_color(self, color_tuple):
		try:
			color, weight = color_tuple
			self._error_color = color
			self._error_weight = weight
		except ValueError as e:
			print e.message

	error_color = AliasProperty(_get_error_color, _set_error_color, bind=('_error_color', '_error_weight', ))
	""":attr:`error_color` holds the color used for error text messages.

	To change the :attr:`error_color` use::

		self.theme_cls.error_color = ['Red', '900']

	The :attr:`error_color` is a
	:class:`kivy.properties.AliasProperty` and defaults to ``Red A700`` in rgb.
	"""

	def __init__(self, **kwargs):
		super(ThemeManager, self).__init__(**kwargs)

		for font in FONTS:
			LabelBase.register(**font)


class ThemeBehaviour(object):
	""":class:`ThemeBehaviour` is a mixin class to make widgets aware of
	an existing theme. This is used by all widgets in this theme, for example
	:class:`kivymd.label.MaterialLabel()`::

		class MaterialLabel(ThemeBehaviour, Label, BackgroundColorCapableWidget)

	.. note::
		If the main app doesn't have the :attr:`theme_cls` attribute, a widget with
		a :class:`ThemeBehaviour` will initiate an instance of :class:`ThemeManager()`
		and use the default settings.
	"""

	auto_color = BooleanProperty(True)
	"""If True, the widget will automatically try to check the color of the background
	in order to decide whether to use a dark or light text color.

	The :attr:`auto_color` is a
	:class:`kivy.properties.BooleanProperty` and defaults to ``True``.
	"""

	def _is_light(self):
		if hasattr(self, 'has_background'):
			if self.has_background:
				return is_light_color(self.background_color)

		parent = self
		while True:
			parent = parent.parent
			if hasattr(parent, 'has_background'):
				if parent.has_background and self.collide_widget(parent):
					return is_light_color(parent.background_color)
					break
			if not hasattr(parent, 'parent'):
				break

		return True

	has_light_background = AliasProperty(_is_light, bind=None)
	"""Check if the widgets background color is light.

	"""

	_theme_cls = ObjectProperty()

	def __init__(self, **kwargs):
		if hasattr(App.get_running_app(), 'theme_cls'):
			self._theme_cls = App.get_running_app().theme_cls
		else:
			self._theme_cls = ThemeManager()
		super(ThemeBehaviour, self).__init__(**kwargs)
