# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, OptionProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivy.clock import Clock

from kivymd import material_resources as m_res
from layouts import MaterialBoxLayout
from label import MaterialLabel
from button import MaterialIconButton
from theme import ThemeBehaviour
from elevationbehaviour import ElevationBehaviour


toolbar_kv = '''
<Toolbar>:
	canvas.before:
		Color:
			rgba: self.background_color
		Rectangle:
			size: self.size
			pos: self.pos

	_nav_button: 		nav_button
	_lbl_title: 		title_label
	_bl_action_buttons:	bl_action_buttons

	size_hint_y:	None
	height:			dp(56)
	padding:		dp(8), 0
	spacing:		dp(8)

	AnchorLayout:
		anchor_x:	'center'
		anchor_y:	'center'
		size_hint:	None, 1
		width:		dp(48) if root.nav_button else 0
		MaterialIconButton:
			id:				nav_button
			size_hint:		None, None
			size:			0, 0
			theme_style:	root.icons_theme_style

	MaterialLabel:
		id: 				title_label
		font_style:			'Subhead'
		theme_text_color:	'Primary'
		theme_style:		root.title_theme_style
		text:				root.title
		padding:			0, dp(20)
		halign:				'left'
		valign:				'middle'
		size_hint_x:		None
		width:				self.texture_size[0]
		text_size:			None, self.height

	AnchorLayout:
		anchor_x:	'right'
		anchor_y:	'center'
		GridLayout:
			id:				bl_action_buttons
			rows:			1
			width:			self.minimum_width
			size_hint:		None, None
			height:			dp(48)
'''
Builder.load_string(toolbar_kv)

class Toolbar(ThemeBehaviour, ElevationBehaviour, BoxLayout):
	"""A toolbar as found on many Material Design/Android apps

	.. warning::
		At initialization the toolbar will follow Material Design's size specs
		for landscape mode apps.
	"""

	title = StringProperty("Title")
	"""String displayed in the toolbar, defaults to "Title"

	Example:
		"My application"
	"""

	nav_button = ListProperty(None, allownone=True)
	"""Button left of the title, value must be a list with icon char and
	 callback

	If the icon (first value) is set to None the button will be hidden.

	Example:
		("md-view-headline", self.my_callback_method)
	"""

	title_theme_style = OptionProperty(None, options=['Light', 'Dark'], allownone=True)

	icons_theme_style = OptionProperty(None, options=['Light', 'Dark'], allownone=True)

	_lbl_title = ObjectProperty()
	_nav_button = ObjectProperty()
	_action_buttons = ListProperty([])
	_bl_action_buttons = ObjectProperty()
	def __init__(self, **kwargs):
		super(Toolbar, self).__init__(**kwargs)
		self.background_color = self._theme_cls.primary_color

	def on_nav_button(self, instance, value):
		if value[0] == '':
			self._nav_button.size = (0, 0)
		else:
			self._nav_button.icon = value[0]
			self._nav_button.size = (dp(48), dp(48))
		if value[1] == None:
			self._nav_button.unbind(on_release=self._nav_button.on_release)
		else:
			self._nav_button.on_release = value[1]

	def add_action_button(self, icon, action=None):
		"""Add an action button to the right of the toolbar.

		:param icon: Unicode character for the icon
		:type icon: str or None
		:param action: Function set to trigger when on_release fires
		:type action: function or None
		"""
		button = MaterialIconButton(size_hint=(None, None),
									size=(dp(48), dp(48)),
									icon=icon)
		if action:
			button.bind(on_release=action)
		button.theme_style = self.icons_theme_style
		self._action_buttons.append(button)

	def get_action_buttons(self):
		"""Returns all action buttons on the toolbar."""
		return self._action_buttons

	def delete_action_button(self, button_widget):
		"""Deletes from the toolbar the provided action button.

		:param button_widget: The action button instance.
		:type button_widget: MaterialIconButton
		"""
		self._bl_action_buttons.remove_widget(button_widget)
		self._action_buttons.remove(button_widget)

	def clear_action_buttons(self):
		self._bl_action_buttons.clear_widgets()
		self._action_buttons = []

	def on__action_buttons(self, *args):
		self._bl_action_buttons.clear_widgets()
		for i in self._action_buttons:
			self._bl_action_buttons.add_widget(i)
