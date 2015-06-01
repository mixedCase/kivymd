# -*- coding: utf-8 -*-
import kivy
import kivymd

kivy.require('1.9.0')
from kivy.lang import Builder
from kivy.app import App
from kivy.metrics import dp
from kivy.properties import ListProperty, ObjectProperty
from kivymd.toolbar import Toolbar
from kivymd.navigationdrawer import NavigationDrawer
from kivymd.button import RaisedButton, FlatButton, FloatingActionButton
from kivymd.dialog import Dialog
from kivymd.label import MaterialLabel
from kivymd.theme import ThemeBehaviour, ThemeManager
from kivymd import images_path
from kivymd.avatar import Avatar

from kivymd.list import MaterialList, TextTile
from kivymd.selectioncontrols import MaterialCheckBox, MaterialSwitch


kitchen_sink_kv = '''
RelativeLayout:
	toolbar: 		_toolbar
	r_btn_1:		_r_btn_1
	dialog_btn:		_diag_btn
	elev_lbl:		_elev_lbl
	nav: 			_nav

	canvas:
		Color:
			rgba: app.theme_cls.main_background_color
		Rectangle:
			size: app.theme_cls.window_size

	Toolbar:
		id: _toolbar
		title:				"KivyMD Kitchen Sink"
		title_theme_style:	'Dark'
		icons_theme_style:	'Dark'
		elevation:			6
		pos_hint:			{'x': 0, 'top': 1}


	RaisedButton:
		id:					_r_btn_1
		text: 				"Enable button"
		size_hint:			None, None
		size:				dp(130), dp(36)
		pos_hint:			{'center_x': 0.3, 'center_y': 0.8}
		elevation_normal:	2
		theme_style:		'Dark'
		disabled:			False

	MaterialLabel:
		id:					_elev_lbl
		text:				"Elevation: " + str(_r_btn_1.elevation)
		font_style:			'Body1'
		size_hint:			None, None
		width:				dp(100)
		height:				self.texture_size[1]
		text_size:			self.width, None
		halign:				'center'
		pos_hint:			{'center_x': 0.3, 'center_y': 0.75}

	RaisedButton:
		id:					_diag_btn
		text: 				"Open dialog"
		size_hint:			None, None
		size:				dp(108), dp(36)
		pos_hint:			{'center_x': 0.7, 'center_y': 0.8}
		elevation_normal:	6
		theme_style:		'Dark'
		disabled:			True

	MaterialList:
		title:						"A avatar+text tile list"
		tile_rows:					2
		list_type:					'avatar_text'
		list_data:					app.tile_avatar_data
		allow_empty_selection:		False
		text_color_selected:		app.theme_cls.primary_dark
		background_color_selected:	(1, 1, 1, 0)
		size_hint:					0.8, None
		height:						dp(300)
		pos_hint:					{'center_x': 0.5, 'center_y': 0.45}

	MaterialCheckBox:
		id:							chkbox
		size_hint:					None, None
		size:						dp(48), dp(48)
		pos_hint:					{'center_x': 0.2, 'center_y': 0.15}
	MaterialLabel:
		text:				"MaterialCheckbox is " + ("active" if chkbox.active else "inactive")
		font_style:			'Body1'
		size_hint:			None, None
		width:				dp(120)
		height:				dp(40)
		text_size:			self.size
		halign:				'center'
		valign:				'middle'
		pos_hint:			{'center_x': 0.2, 'center_y': 0.09}


	# FloatingActionButton:
	# 	size_hint:			None, None
	# 	size:				dp(48), dp(48)
	# 	pos_hint:			{'center_x': 0.6, 'center_y': 0.15}
	# 	theme_style:		'Dark'
	# MaterialSwitch:
	# 	id:							switch
	# 	size_hint:					None, None
	# 	size:						dp(24), dp(24)
	# 	pos_hint:					{'center_x': 0.6, 'center_y': 0.15}
	# MaterialLabel:
	# 	text:				"MaterialSwitch is " + ("active" if switch.active else "inactive")
	# 	font_style:			'Body1'
	# 	size_hint:			None, None
	# 	width:				dp(120)
	# 	height:				dp(40)
	# 	text_size:			self.size
	# 	halign:				'center'
	# 	valign:				'middle'
	# 	pos_hint:			{'center_x': 0.6, 'center_y': 0.09}

	# MaterialList:
	# 	title:						"A 2-row text tile list"
	# 	tile_rows:					2
	# 	list_type:					'text'
	# 	list_data:					app.tile_data
	# 	text_color_selected:		app.theme_cls.primary_dark
	# 	background_color_selected:	(1, 1, 1, 0)
	# 	size_hint:					0.8, None
	# 	height:						dp(180)
	# 	pos_hint:					{'center_x': 0.5, 'center_y': 0.5}

	# MaterialList:
	# 	title:						"An icon+text tile list"
	# 	tile_rows:					2
	# 	list_type:					'icon_text'
	# 	list_data:					app.tile_icon_data
	# 	allow_empty_selection:		False
	# 	text_color_selected:		app.theme_cls.primary_dark
	# 	background_color_selected:	(1, 1, 1, 0)
	# 	size_hint:					0.8, None
	# 	height:						dp(200)
	# 	pos_hint:					{'center_x': 0.5, 'center_y': 0.3}

	# MaterialList:
	# 	title:						"A single row text tile list"
	# 	tile_rows:					1
	# 	list_type:					'text'
	# 	list_data:					app.tile_single_data
	# 	allow_empty_selection:		False
	# 	text_color_selected:		app.theme_cls.primary_dark
	# 	background_color_selected:	(1, 1, 1, 0)
	# 	size_hint:					0.8, None
	# 	height:						dp(200)
	# 	pos_hint:					{'center_x': 0.5, 'center_y': 0.3}


	NavigationDrawer:
		id: 				_nav
		side:				'left'
		MaterialList:
			tile_rows:					2
			list_type:					'icon_text'
			list_data:					app.tile_icon_data
			allow_empty_selection:		False
			text_color_selected:		app.theme_cls.primary_dark
			background_color_selected:	(1, 1, 1, 0)
			divider_color:				app.theme_cls.divider_color()
			size_hint:					1, None
			height:						dp(340)

'''


class KitchenSink(App):
	theme_cls = ThemeManager()

	tile_data = ListProperty([])

	tile_single_data = ListProperty([])

	tile_icon_data = ListProperty()

	tile_avatar_data = ListProperty()

	nav = ObjectProperty()

	def __init__(self, **kwargs):
		super(KitchenSink, self).__init__(**kwargs)
		self.theme_cls.primary_palette = 'Green'
		self.theme_cls.accent_palette = 'Teal'
		self.theme_cls.theme_style = 'Light'

	def on_start(self):
		pass

	def build(self):
		root = Builder.load_string(kitchen_sink_kv)
		root.toolbar.nav_button = ["md-menu", lambda *x: root.nav.toggle()]

		root.toolbar.add_action_button("md-refresh")
		root.toolbar.add_action_button("md-more-vert")

		root.r_btn_1.bind(on_release=lambda *x: setattr(root.dialog_btn, 'disabled', not root.dialog_btn.disabled))
		self.tile_data = [{'text': "Button 1", 'secondary_text': "With a secondary text"},
						  {'text': "Button 2", 'secondary_text': "With a secondary text"},
						  {'text': "Button 3", 'secondary_text': "With a secondary text"},
						  {'text': "Button 4", 'secondary_text': "With a secondary text"}]

		self.tile_single_data = [{'text': "Button 1"},
								  {'text': "Button 2"},
								  {'text': "Button 3"},
								  {'text': "Button 4"}]

		self.tile_icon_data = [{'icon': 'md-alarm', 'text': 'Alarm',
							   'secondary_text': "An alarm button",
								'callback': root.nav.dismiss},
							  {'icon': 'md-event', 'text': 'Event',
							   'secondary_text': "An event button",
								'callback': root.nav.dismiss},
							  {'icon':  'md-search', 'text': 'Search',
							   'secondary_text': "A search button",
								'callback': root.nav.dismiss},
							  {'icon': 'md-thumb-up', 'text': 'Like',
							   'secondary_text': "A like button",
								'callback': root.nav.dismiss}]

		self.tile_avatar_data = [{'avatar': images_path + 'default_avatar.jpg', 'text': 'Avatar tile',
								   'secondary_text': "That's a handsome dude!"},
								  {'avatar': images_path + 'default_avatar.jpg', 'text': 'Avatar tile',
								   'secondary_text': "Very handsome indeed"},
								  {'avatar':  images_path + 'default_avatar.jpg', 'text': 'Avatar tile',
								   'secondary_text': "Extraordinary handsome"},
								  {'avatar': images_path + 'default_avatar.jpg', 'text': 'Avatar tile',
								   'secondary_text': "Super handsome"}]

		content = MaterialLabel(font_style='Body1',
								theme_text_color='Secondary',
								text="This is a Dialog with a title and some text. That's pretty awesome right!",
								valign='top')

		content.bind(size=content.setter('text_size'))

		self.dialog = Dialog(title="This is a test dialog",
							 content=content,
							 size_hint=(.8, None),
							 height=dp(200),
							 auto_dismiss=True)

		self.dialog.add_action_button("Dismiss", action=lambda *x: self.dialog.dismiss())

		root.dialog_btn.bind(on_release=self.dialog.open)

		return root

	def on_pause(self):
		return True

	def on_stop(self):
		pass


if __name__ == '__main__':
	KitchenSink().run()