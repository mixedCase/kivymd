# -*- coding: utf-8 -*-
import kivymd
from kivy.metrics import dp
from kivy.core.window import Window
from kivy import platform
from copy import deepcopy

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

# While theming is not implemented, use light background settings
TEXT_COLOR = (0,0,0,1)
SECONDARY_TEXT_COLOR = (0,0,0,0.54)

LIST_VERTICAL_PADDING = dp(8)

PALETTE_RED = {
	"50": [255/255., 235/255., 238/255.],
	"100": [255/255., 205/255., 210/255.],
	"200": [239/255., 154/255., 154/255.],
	"300": [229/255., 115/255., 115/255.],
	"400": [239/255., 83/255., 80/255.],
	"500": [244/255., 67/255., 54/255.],
	"600": [229/255., 57/255., 53/255.],
	"700": [211/255., 47/255., 47/255.],
	"800": [198/255., 40/255., 40/255.],
	"900": [183/255., 28/255., 28/255.],
	"A100": [255/255., 138/255., 128/255.],
	"A200": [255/255., 82/255., 82/255.],
	"A400": [255/255., 23/255., 68/255.],
	"A700": [213/255., 0/255., 0/255.],
}

PALETTE_TEAL = {
	"50": [224/255., 242/255., 241/255.],
	"100": [178/255., 223/255., 219/255.],
	"200": [128/255., 203/255., 196/255.],
	"300": [77/255., 182/255., 172/255.],
	"400": [38/255., 166/255., 154/255.],
	"500": [0/255., 150/255., 136/255.],
	"600": [0/255., 137/255., 123/255.],
	"700": [0/255., 121/255., 107/255.],
	"800": [0/255., 105/255., 92/255.],
	"900": [0/255., 77/255., 64/255.],
	"A100": [167/255., 255/255., 235/255.],
	"A200": [100/255., 255/255., 218/255.],
	"A400": [29/255., 233/255., 182/255.],
	"A700": [0/255., 191/255., 165/255.],
}

PALETTE_GREY = {
	"50": [250/255., 250/255., 250/255.],
	"100": [245/255., 245/255., 245/255.],
	"200": [238/255., 238/255., 238/255.],
	"300": [224/255., 224/255., 224/255.],
	"400": [189/255., 189/255., 189/255.],
	"500": [158/255., 158/255., 158/255.],
	"600": [117/255., 117/255., 117/255.],
	"700": [97/255., 97/255., 97/255.],
	"800": [66/255., 66/255., 66/255.],
	"900": [33/255., 33/255., 33/255.],
}

# Gallery available here:
# https://zavoloklom.github.io/material-design-iconic-font/icons.html
ICONS = {
	"md-menu": "",
    "md-refresh": ""
}

def get_palette_with_alpha(palette, alpha_level=1.):
	new_palette = deepcopy(palette)
	for i in palette:
		new_palette[i].append(alpha_level)
	return new_palette

def get_primary_palette():
	raise NotImplementedError