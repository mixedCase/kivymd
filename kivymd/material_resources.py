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
FONT_REGULAR = kivymd.fonts_path + "Roboto-Regular.ttf"
FONT_MEDIUM = kivymd.fonts_path + "Roboto-Medium.ttf"
FONT_BOLD = kivymd.fonts_path + "Roboto-Bold.ttf"
FONT_ICONS = kivymd.fonts_path + "Material-Design-Iconic-Font.ttf"
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



# While theming is not implemented, use light background settings
TEXT_COLOR = (0, 0, 0, 1)
SECONDARY_TEXT_COLOR = (0, 0, 0, 0.54)

LIST_VERTICAL_PADDING = dp(8)

PALETTE_RED = {
	"50": [255 / 255., 235 / 255., 238 / 255.],
	"100": [255 / 255., 205 / 255., 210 / 255.],
	"200": [239 / 255., 154 / 255., 154 / 255.],
	"300": [229 / 255., 115 / 255., 115 / 255.],
	"400": [239 / 255., 83 / 255., 80 / 255.],
	"500": [244 / 255., 67 / 255., 54 / 255.],
	"600": [229 / 255., 57 / 255., 53 / 255.],
	"700": [211 / 255., 47 / 255., 47 / 255.],
	"800": [198 / 255., 40 / 255., 40 / 255.],
	"900": [183 / 255., 28 / 255., 28 / 255.],
	"A100": [255 / 255., 138 / 255., 128 / 255.],
	"A200": [255 / 255., 82 / 255., 82 / 255.],
	"A400": [255 / 255., 23 / 255., 68 / 255.],
	"A700": [213 / 255., 0 / 255., 0 / 255.],
}

PALETTE_TEAL = {
	"50": [224 / 255., 242 / 255., 241 / 255.],
	"100": [178 / 255., 223 / 255., 219 / 255.],
	"200": [128 / 255., 203 / 255., 196 / 255.],
	"300": [77 / 255., 182 / 255., 172 / 255.],
	"400": [38 / 255., 166 / 255., 154 / 255.],
	"500": [0 / 255., 150 / 255., 136 / 255.],
	"600": [0 / 255., 137 / 255., 123 / 255.],
	"700": [0 / 255., 121 / 255., 107 / 255.],
	"800": [0 / 255., 105 / 255., 92 / 255.],
	"900": [0 / 255., 77 / 255., 64 / 255.],
	"A100": [167 / 255., 255 / 255., 235 / 255.],
	"A200": [100 / 255., 255 / 255., 218 / 255.],
	"A400": [29 / 255., 233 / 255., 182 / 255.],
	"A700": [0 / 255., 191 / 255., 165 / 255.],
}

PALETTE_GREY = {
	"50": [250 / 255., 250 / 255., 250 / 255.],
	"100": [245 / 255., 245 / 255., 245 / 255.],
	"200": [238 / 255., 238 / 255., 238 / 255.],
	"300": [224 / 255., 224 / 255., 224 / 255.],
	"400": [189 / 255., 189 / 255., 189 / 255.],
	"500": [158 / 255., 158 / 255., 158 / 255.],
	"600": [117 / 255., 117 / 255., 117 / 255.],
	"700": [97 / 255., 97 / 255., 97 / 255.],
	"800": [66 / 255., 66 / 255., 66 / 255.],
	"900": [33 / 255., 33 / 255., 33 / 255.],
}

# Gallery available here:
# https://zavoloklom.github.io/material-design-iconic-font/icons.html
ICONS = {
	"md-menu": "",
	"md-refresh": ""
}


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

def get_btn_down_color(color=[]):
	color_tuple = get_color_tuple(color)
	ordered_palette = OrderedDict(sorted(colors[color_tuple[0]].items(), key=lambda x: int(x[0][1:]) if str.isalpha(x[0][:1]) else int(x[0])))
	index = ordered_palette.keys().index(color_tuple[1])
	try:
		return get_rgba_color([color_tuple[0], ordered_palette.items()[index + 2][0]])
	except:
		return (0, 0, 0, 1)


def is_light_color(color=[]):
	if len(color) == 2:
		return True if color[1] in light_colors[color[0]] else False
	elif len(color) > 2:
		color_tuple = get_color_tuple(color)
		if len(color_tuple) == 2:
			return True if color_tuple[1] in light_colors[color_tuple[0]] else False
	return True


def get_palette_with_alpha(palette, alpha_level=1.):
	new_palette = deepcopy(palette)
	for i in palette:
		new_palette[i].append(alpha_level)
	return new_palette


def get_primary_palette():
	raise NotImplementedError