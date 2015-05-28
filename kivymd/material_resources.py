# -*- coding: utf-8 -*-
import kivymd
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy import platform
from copy import deepcopy
from kivymd.md_icon_definitions import md_icons
from kivymd.color_definitions import colors, light_colors

# Feel free to override this const if you're designing for a device such as
# a GNU/Linux tablet.
if platform != "android" and platform != "ios":
	DEVICE_TYPE = "desktop"
elif Window.width >= dp(600) and Window.height >= dp(600):
	DEVICE_TYPE = "tablet"
else:
	DEVICE_TYPE = "mobile"

if DEVICE_TYPE == "mobile":
	MAX_NAV_DRAWER_WIDTH = dp(320)
	HORIZ_MARGINS = dp(16)
	STANDARD_INCREMENT = dp(56)
	PORTRAIT_TOOLBAR_HEIGHT = STANDARD_INCREMENT
	LANDSCAPE_TOOLBAR_HEIGHT = STANDARD_INCREMENT - dp(8)
else:
	MAX_NAV_DRAWER_WIDTH = dp(400)
	HORIZ_MARGINS = dp(24)
	STANDARD_INCREMENT = dp(64)
	PORTRAIT_TOOLBAR_HEIGHT = STANDARD_INCREMENT
	LANDSCAPE_TOOLBAR_HEIGHT = STANDARD_INCREMENT

TOUCH_TARGET_HEIGHT = dp(48)
FONT_REGULAR = kivymd.fonts_path + "Roboto-Regular.ttf"
FONT_MEDIUM = kivymd.fonts_path + "Roboto-Medium.ttf"
FONT_BOLD = kivymd.fonts_path + "Roboto-Bold.ttf"
FONT_ICONS = kivymd.fonts_path + "Material-Design-Iconic-Font.ttf"
ICON_DEFAULT = kivymd.images_path + "ic_lens_grey_48dp.png"

# FIXME:  While theming is not implemented, use light background settings
TEXT_COLOR = (0,0,0,1)
SECONDARY_TEXT_COLOR = (0,0,0,0.54)

LIST_VERTICAL_PADDING = dp(8)

FONTS = [
    {
        "name": "Roboto",
        "fn_regular": kivymd.fonts_path + 'Roboto-Regular.ttf',
        "fn_bold": kivymd.fonts_path + 'Roboto-Medium.ttf',
		"fn_italic": kivymd.fonts_path + 'Roboto-Italic.ttf',
		"fn_bolditalic": kivymd.fonts_path + 'Roboto-MediumItalic.ttf'
    },
    {
        "name": "RobotoLight",
        "fn_regular": kivymd.fonts_path + 'Roboto-Thin.ttf',
		"fn_bold": kivymd.fonts_path + 'Roboto-Light.ttf',
		"fn_italic": kivymd.fonts_path + 'Roboto-ThinItalic.ttf',
		"fn_bolditalic": kivymd.fonts_path + 'Roboto-LightItalic.ttf'
    },
	{
        "name": "Icons",
        "fn_regular": kivymd.fonts_path + 'Material-Design-Iconic-Font.ttf'
    }
]


def get_icon_char(icon):
	if icon != '':
		try:
			return md_icons[icon]
		except:
			print('icon: ' + icon + ' not in md_icons')
			return ''
	else:
		return ''

def get_rgba_color(color_tuple, control_alpha=None):
	color, weight = color_tuple
	try:
		color = get_color_from_hex(colors[color][weight])
	except:
		print("Error: {} and/or {} not found, set to default".format(color, weight))
		return (1., 1., 1., 1.)
	if control_alpha is None:
		return color
	else:
		color[3] = control_alpha
		return color

def get_palette_with_alpha(palette, alpha_level=1.):
	new_palette = deepcopy(palette)
	for i in palette:
		new_palette[i].append(alpha_level)
	return new_palette

def get_primary_palette():
	raise NotImplementedError