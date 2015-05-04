# -*- coding: utf-8 -*-
__version__ = "0.0.1"

'''
ThemeManager
============

The :class:`ThemeManager()` manage the overall appearance by implementing the Material
Design style guidelines for colors and fonts.

.. note::
    This is a work in progress and not a complete implementation of all the parts of
    the official Material Design.

To create an instance of the Theme Manager in you app:

    from kivymd.theme import ThemeManager

    # Create the manager
    theme_manager = ThemeManager()


Theme style
-----------

The Material theme comes in two styles, 'Light' and 'Dark'. This setting defines the
background color of the app.

    # Set the overall theme style by choosing between 'Light' or 'Dark'
    theme_manager.theme_style = 'Dark'

This will determine the background colors and text colors:

    :attr:`main_background_color` - This is the main background color for the app.

    .. note::
        'Light' - Grey 200
        'Dark' - #303030


    :attr:`dialog_background_color` - This is the background color used by
    :class:`MaterialDialog()` and :class:`MaterialCard`.

    .. note::
        'Light' - Grey 50
        'Dark' - Grey 800


Theme colors
------------

The rest of the user interface uses colors from a pre-defined set of colors organized
in 'palettes'. The :class:`ThemeManager()` handles two palettes, one for the primary colors
and one for the accent colors.

    # Set the primary color palette
    theme_manager.primary_palette = 'Blue'

These color palettes comprises primary and accent colors that can be used for illustration or
to develop your brand colors. They’ve been designed to work harmoniously with each other.

Each palette is divided into 10 primary colors ('50', '100' ... '900') and 4 accent
colors ('A100', 'A200', 'A400' and 'A700). These colors are different hues of the main color
and are combined in a specific manner in order to keep the theme consistent:

    :attr:`primary_color` is by default the 500 hue of the primary color palette

    :attr:`primary_dark` is by default the 700 hue of the primary color palette

    :attr:`primary_light` is by default the 100 hue of the primary color palette

.. warning::
    The palettes 'Brown', 'Grey' and 'BlueGrey' doesn't have any accent colors.

It's recommended not to use more than three different hues of the primary color. However, the
default hues can be customized.

    # Set the primary color hue to '400'
    theme_manager.primary_hue = '400'

    # Set the primary dark hue to '900'
    theme_manager.primary_dark_hue = '900'

    # Set the primary light hue to '200'
    theme_manager.primary_light_hue = '200'

The :attr:`accent_palette` is used to set the accent color in the app:

    # Set the accent color to 'Red'
    theme_manager.accent_palette = 'Red'

The :attr:`accent_color` should be used for primary action buttons and components
like switches or sliders. The main accent color uses the 'A200' hue but if
the background is too light or dark there are two fallback colors that can
be used instead:

    :attr:`accent_dark` is by default the 'A400' hue of the accent color

    :attr:`accent_light` is by default the 'A100' hue of the accent color

These default accent color hues can also be customized:

    # Set the accent color main hue to 'A400'
    theme_manager.accent_hue = 'A400'

    # Set the darker fallback accent color to 'A700'
    theme_manager.accent_dark_hue = 'A700'


Text color
-----------

The color of the text within the app is determined primarily by the :attr:`theme_style`.
Different text blocks should be separated by their importance relative to other text:

    :attr:`primary_text_color` - This is the primary color for text blocks.

    .. note::
        :attr:`theme_style('Light')` - 87% black
        :attr:`theme_style('Dark')` - 100% white


    :attr:`secondary_text_color` - This is the secondary color that should be used for
    text that's not as important as other text.

    .. note::
        :attr:`theme_style('Light')` - 54% black
        :attr:`theme_style('Dark')` - 70% white


    :attr:`hint_text_color` - This is the color used for hint text by :class:`MaterialTextInput()`.

    .. note::
        :attr:`theme_style('Light')` - 26% black
        :attr:`theme_style('Dark')` - 30% white


    :attr:`disabled_color` is the same color as :attr:`hint_text_color` and should be used for
    disabled widgets such as :class:`MaterialFlatButton()`.


    :attr:`divider_color` - This is the color used by :class:`Divider()`.

    .. note::
        :attr:`theme_style('Light')` - 12% black
        :attr:`theme_style('Dark')` - 12% white


Please read the official documentation for more information:
http://www.google.com/design/spec/material-design/introduction.html

'''


from kivy.properties import StringProperty, OptionProperty, AliasProperty, ListProperty
from kivymd.material_resources import get_rgba_color

class ThemeManager(object):

    theme_style = OptionProperty('Light', options=['Light', 'Dark'])
    '''Set the overall color scheme. Available options are 'Light' and 'Dark' and will
    determine :attr:`main_background_color` and :attr:`dialog_background_color`.

    The :attr:`theme_style` is a
    :class:`~kivy.properties.OptionProperty` and defaults to 'Light'.
    '''

    def _get_main_background_color(self):
        return get_rgba_color([self.theme_style, 'MainBackground'])

    main_background_color = AliasProperty(_get_main_background_color, bind('theme_style'))
    '''The :attr:`main_background_color` holds the main background color. This is determined
    by the :attr:`theme_style`:

    'Light' - Grey 200
    'Dark' - #303030

    The :attr:`main_background_color` is a
    :class:`~kivy.properties.AliasProperty` and defaults to 'Grey 200' in rgb.
    '''

    def _get_dialog_background_color(self):
        return get_rgba_color([self.theme_style, 'DialogBackground'])

    dialog_background_color = AliasProperty(_get_dialog_background_color, bind('theme_style'))
    '''The :attr:`dialog_background_color` holds the background color used by :class:`MaterialDialog()`
    and :class:`MaterialCard()`. This is determined by the :attr:`theme_style`:

    'Light' - Grey 50
    'Dark' - Grey 800

    The :attr:`main_background_color` is a
    :class:`~kivy.properties.AliasProperty` and defaults to 'Grey 200' in rgb.
    '''

    primary_palette = OptionProperty('Grey', options=['Pink', 'Blue', 'Indigo', 'BlueGrey', 'Brown', 'LightBlue', 'Purple',
                                                      'Grey', 'Yellow', 'LightGreen', 'DeepOrange', 'Green', 'Red', 'Teal',
                                                      'Orange', 'Cyan', 'Amber', 'DeepPurple', 'Lime'])
    '''The primary color palette. A Material Design theme is by default limited
    to three hues of the :attr:`primary_palette`:

    500 - the default hue that will be used for the :class:kivymd.`Toolbar` and
    should be used for other larger color blocks.

    700 - a darker hue.

    100 - a lighter hue.

    These hues can be customized by setting :attr:`primary_hue`, :attr:`primary_dark_hue`
    and :attr:`primary_light_hue`.

    :attr:`primary_color` holds the primary color of the currently selected primary
     palette (in rgb).

    :attr:`primary_dark` holds the dark hue of the currently selected primary
     palette (in rgb).

    :attr:`primary_light` holds the light hue of the currently selected primary
     palette (in rgb).

    The :attr:`primary_palette` is a
    :class:`~kivy.properties.OptionProperty` and defaults to 'Grey'.
    '''

    primary_hue = OptionProperty('500', options=['50', '100', '200', '300', '400', '500', '600', '700', '800',
                                                  '900', 'A100', 'A200', 'A400', 'A700'])
    '''The :attr:`primary_hue` holds the default hue for the primary color palette.

    The :attr:`primary_hue` is a
    :class:`~kivy.properties.OptionProperty` and defaults to '500'.
    '''

    primary_dark_hue = OptionProperty('700', options=['50', '100', '200', '300', '400', '500', '600', '700', '800',
                                                  '900', 'A100', 'A200', 'A400', 'A700'])
    '''The :attr:`primary_dark_hue` holds the darker hue for the primary color palette.

    The :attr:`primary_dark_hue` is a
    :class:`~kivy.properties.OptionProperty` and defaults to '700'.
    '''

    primary_light_hue = OptionProperty('100', options=['50', '100', '200', '300', '400', '500', '600', '700', '800',
                                                  '900', 'A100', 'A200', 'A400', 'A700'])
    '''The :attr:`primary_light_hue` holds the darker hue for the primary color palette.

    The :attr:`primary_light_hue` is a
    :class:`~kivy.properties.OptionProperty` and defaults to '100'.
    '''

    def _get_primary_color(self):
        return get_rgba_color([self.primary_palette, self.primary_hue])

    primary_color = AliasProperty(_get_primary_color, bind=('primary_palette', 'primary_hue'))
    '''The :attr:`primary_color` holds the primary 500 hue of the currently selected
    :attr:`primary_palette` in rgb.

    The :attr:`primary_color` is a
    :class:`~kivy.properties.AliasProperty` and defaults to 'Grey 500' in rgb format.
    '''

    def _get_primary_dark(self):
        return get_rgba_color([self.primary_palette, self.primary_dark_hue])

    primary_dark = AliasProperty(_get_primary_dark, bind=('primary_palette', 'primary_dark_hue'))
    '''The :attr:`primary_dark` holds the darker 700 hue of the currently selected
    :attr:`primary_palette` in rgb.

    The :attr:`primary_dark` is a
    :class:`~kivy.properties.AliasProperty` and defaults to 'Grey 700' in rgb format.
    '''

    def _get_primary_light(self):
        return get_rgba_color([self.primary_palette, self.primary_light_hue])

    primary_light = AliasProperty(_get_primary_light, bind=('primary_palette', 'primary_light_hue'))
    '''The :attr:`primary_light` holds the lighter 100 hue of the currently selected
    :attr:`primary_palette` in rgb.

    The :attr:`primary_light` is a
    :class:`~kivy.properties.AliasProperty` and defaults to 'Grey 100' in rgb format.
    '''

    accent_palette = OptionProperty('Teal', options=['Pink', 'Blue', 'Indigo', 'BlueGrey', 'Brown', 'LightBlue', 'Purple',
                                                      'Grey', 'Yellow', 'LightGreen', 'DeepOrange', 'Green', 'Red', 'Teal',
                                                      'Orange', 'Cyan', 'Amber', 'DeepPurple', 'Lime'])
    '''The accent color palette. Use the accent color for your primary action
    button and components like switches or sliders.

    If your accent color is too light or dark for the background color, choose
    :attr:`accent_light` or :attr:`accent_dark` as a fallback for these cases.

    The default accent color hue is A200, for the lighter fallback A100 and for
    the darker fallback A400. These hues can be customized by setting
    :attr:`accent_light_hue` and :attr:`accent_dark_hue`.

    :attr:`accent_color` holds the currently selected accent color (in rgb).

    Use :attr:`accent_light` holds the lighter fallback hue of the currently selected
    accent color (in rgb).

    Use :attr:`accent_dark` holds the darker fallback hue of the currently selected
    accent color (in rgb).

    The :attr:`accent_palette` is a
    :class:`~kivy.properties.OptionProperty` and defaults to 'Teal'.
    '''

    accent_hue = OptionProperty('A200', options=['50', '100', '200', '300', '400', '500', '600', '700', '800',
                                                  '900', 'A100', 'A200', 'A400', 'A700'])
    '''The :attr:`accent_hue` holds the default hue for the accent color palette.

    The :attr:`accent_hue` is a
    :class:`~kivy.properties.OptionProperty` and defaults to 'A200'.
    '''

    accent_light_hue = OptionProperty('A100', options=['50', '100', '200', '300', '400', '500', '600', '700', '800',
                                                  '900', 'A100', 'A200', 'A400', 'A700'])
    '''The :attr:`accent_light_hue` holds the lighter fallback hue for the
    accent color palette.

    The :attr:`accent_light_hue` is a
    :class:`~kivy.properties.OptionProperty` and defaults to 'A100'.
    '''

    accent_dark_hue = OptionProperty('A400', options=['50', '100', '200', '300', '400', '500', '600', '700', '800',
                                                  '900', 'A100', 'A200', 'A400', 'A700'])
    '''The :attr:`accent_dark_hue` holds the darker fallback hue for the
    accent color palette.

    The :attr:`accent_dark_hue` is a
    :class:`~kivy.properties.OptionProperty` and defaults to 'A400'.
    '''

    def _get_accent_color(self):
        return get_rgba_color([self.accent_palette, self.accent_hue])

    accent_color = AliasProperty(_get_accent_color, bind=('accent_palette', 'accent_hue'))
    '''The :attr:`accent_color` holds the A200 hue of the currently selected
    :attr:`accent_palette` in rgb.

    The :attr:`accent_color` is a
    :class:`~kivy.properties.AliasProperty` and defaults to 'Teal A200' in rgb format.
    '''

    def _get_accent_light(self):
        return get_rgba_color([self.accent_palette, self.accent_light_hue])

    accent_light = AliasProperty(_get_accent_light, bind=('accent_palette', 'accent_light_hue'))
    '''The :attr:`accent_light` holds the lighter A100 hue of the currently selected
    :attr:`accent_palette` in rgb.

    The :attr:`accent_light` is a
    :class:`~kivy.properties.AliasProperty` and defaults to 'Teal A100' in rgb format.
    '''

    def _get_accent_dark(self):
        return get_rgba_color([self.accent_palette, self.accent_dark_hue])

    accent_dark = AliasProperty(_get_accent_dark, bind=('accent_palette', 'accent_dark_hue'))
    '''The :attr:`accent_dark` holds the darker A400 hue of the currently selected
    :attr:`accent_palette` in rgb.

    The :attr:`accent_dark` is a
    :class:`~kivy.properties.AliasProperty` and defaults to 'Teal A400' in rgb format.
    '''

    def _get_primary_text_color(self):
        if self.theme_style == 'Light':
            return get_rgba_color(['Black', 'Black'], control_alpha=0.87)
        if self.theme_style == 'Dark':
            return get_rgba_color(['White', 'White'], control_alpha=1.0)

    primary_text_color = AliasProperty(_get_primary_text_color, bind=('theme_style'))
    '''The :attr:`primary_text_color` holds the primary text color. This is determined by the
    :attr:`theme_style`:

    'Light' - 87% black
    'Dark' - 100% white

    The :attr:`primary_text_color` is a
    :class:`~kivy.properties.AliasProperty` and defaults to 87% black in rgb.
    '''

    def _get_secondary_text_color(self):
        if self.theme_style == 'Light':
            return get_rgba_color(['Black', 'Black'], control_alpha=0.54)
        if self.theme_style == 'Dark':
            return get_rgba_color(['White', 'White'], control_alpha=0.70)

    secondary_text_color = AliasProperty(_get_secondary_text_color, bind=('theme_style'))
    '''The :attr:`secondary_text_color` holds the secondary text color. This is determined by the
    :attr:`theme_style`:

    'Light' - 54% black
    'Dark' - 70% white

    The :attr:`secondary_text_color` is a
    :class:`~kivy.properties.AliasProperty` and defaults to 54% black in rgb.
    '''

    def _get_hint_text_color(self):
        if self.theme_style == 'Light':
            return get_rgba_color(['Black', 'Black'], control_alpha=0.54)
        if self.theme_style == 'Dark':
            return get_rgba_color(['White', 'White'], control_alpha=0.70)

    hint_text_color = AliasProperty(_get_hint_text_color, bind=('theme_style'))
    '''The :attr:`hint_text_color` holds the hint text color. This is determined by the
    :attr:`theme_style`:

    'Light' - 26% black
    'Dark' - 30% white

    The :attr:`hint_text_color` is a
    :class:`~kivy.properties.AliasProperty` and defaults to 26% black in rgb.
    '''

    disabled_color = AliasProperty(_get_hint_text_color, bind=('hint_text_color'))
    '''The :attr:`disabled_color` is the same as :attr:`hint_text_color` and is only
    there to make thins more clear.

    The :attr:`disabled_color` is a
    :class:`~kivy.properties.AliasProperty` and defaults to 26% black in rgb.
    '''

    def _get_divider_color(self):
        if self.theme_style == 'Light':
            return get_rgba_color(['Black', 'Black'], control_alpha=0.12)
        if self.theme_style == 'Dark':
            return get_rgba_color(['White', 'White'], control_alpha=0.12)

    divider_color = AliasProperty(_get_divider_color, bind=('theme_style'))
    '''The :attr:`divider_color` holds the divider color. This is determined by the
    :attr:`theme_style`:

    'Light' - 12% black
    'Dark' - 12% white

    The :attr:`divider_color` is a
    :class:`~kivy.properties.AliasProperty` and defaults to 12% black in rgb.
    '''


theme_colors = {'ERROR':            get_rgba_color(['Red', 'A700']),
                'WHITE':            get_rgba_color(['White', 'White']),
                'PRIMARY':          get_rgba_color(['LightGreen', '500']),
                'PRIMARY_DARK':     get_rgba_color(['LightGreen', '700']),
                'PRIMARY_LIGHT':    get_rgba_color(['LightGreen', '100']),
                'ACCENT_1':         get_rgba_color(['Red', '500']),
                'ACCENT_2':         get_rgba_color(['Yellow', 'A100']),
                'PRIMARY_TEXT':     get_rgba_color(['Black', 'Black'], control_alpha=.87),
                'SECONDARY_TEXT':   get_rgba_color(['Black', 'Black'], control_alpha=.54),
                'HINTS':            get_rgba_color(['Black', 'Black'], control_alpha=.26),
                'ICONS':            get_rgba_color(['White', 'White']),
                'COLOR_DOWN':       get_color_from_hex('99999966'),
                'DIVIDER':          get_rgba_color(['Black', 'Black'], control_alpha=.12),
                'TRANSPARENT':      (1., 1., 1., 0)
                }