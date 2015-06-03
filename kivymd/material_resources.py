# -*- coding: utf-8 -*-
from collections import OrderedDict
import kivymd
from kivy.metrics import dp
from kivy.core.window import Window
from kivy import platform
from kivy.utils import get_color_from_hex
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
	MAX_NAV_DRAWER_WIDTH = dp(300)
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
ICON_DEFAULT = kivymd.images_path + "ic_lens_grey_48dp.png"


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

LIST_VERTICAL_PADDING = dp(8)


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

def get_hex_from_rgba_color(color):
	hex_values = []

	for component in color:
		hex_values.append(hex(int(component * 255))[2:])

	return ''.join(hex_values)

def get_color_tuple(color=[]):
	hex_color = get_hex_from_rgba_color(color)[:6]
	color_tuple = []
	for name, hues in colors.iteritems():
		for hue, color in hues.iteritems():
			if color == hex_color:
				color_tuple.append(name)
				color_tuple.append(hue)
				return color_tuple
	return []

# def get_btn_down_color(color=[]):
# 	color_tuple = get_color_tuple(color)
# 	ordered_palette = OrderedDict(sorted(colors[color_tuple[0]].items(), key=lambda x: int(x[0][1:]) if str.isalpha(x[0][:1]) else int(x[0])))
# 	index = ordered_palette.keys().index(color_tuple[1])
# 	try:
# 		return get_rgba_color([color_tuple[0], ordered_palette.items()[index + 2][0]])
# 	except:
# 		return (0, 0, 0, 1)