# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, BooleanProperty, ListProperty
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivymd.button import FlatButton
from kivymd.shadow import Shadow
from kivy.animation import Animation
from kivy.clock import Clock
from theme import ThemeBehaviour
from elevationbehaviour import ElevationBehaviour

dialog_kv = '''
<Dialog>:
	canvas:
		Color:
			rgba: 	self._theme_cls.dialog_background_color
		Rectangle:
			size: 	self.size
			pos: 	self.pos

	_container:		container
	_action_area:	action_area
	GridLayout:
		cols:			1
		padding:		dp(24), dp(24), dp(24), 0
		spacing:		dp(20)

		MaterialLabel:
			text:				root.title
			font_style:			'Title'
			theme_text_color:	'Primary'
			halign:				'left'
			valign:				'middle'
			size_hint_y:		None
			text_size:			self.width, None
			height:				self.texture_size[1]

		BoxLayout:
			id:					container

		AnchorLayout:
			anchor_x:			'right'
			anchor_y:			'center'
			size_hint:			1, None
			height:				dp(48)
			padding:			dp(8), dp(8)
			spacing:			dp(4)

			GridLayout:
				id:				action_area
				rows:			1
				size_hint_x:	None
				width:			self.minimum_width
'''



class Dialog(ThemeBehaviour, ElevationBehaviour, ModalView):

	title = StringProperty('')

	content = ObjectProperty(None)

	_container = ObjectProperty()
	_action_buttons = ListProperty([])
	_action_area = ObjectProperty()

	def __init__(self, **kwargs):
		Builder.load_string(dialog_kv)
		super(Dialog, self).__init__(**kwargs)
		self.elevation = 12


	def add_action_button(self, text, action=None):
		"""Add an :class:`FlatButton` to the right of the action area.

		:param icon: Unicode character for the icon
		:type icon: str or None
		:param action: Function set to trigger when on_release fires
		:type action: function or None
		"""
		button = FlatButton(text=text,
							size_hint=(1, None),
							height=dp(36),
							text_color=self._theme_cls.primary_color,
							background_color=self._theme_cls.dialog_background_color)
		if action:
			button.bind(on_release=action)
		self._action_buttons.append(button)

	def add_widget(self, widget):
		if self._container:
			if self.content:
				raise PopupException(
					'Popup can have only one widget as content')
			self.content = widget
		else:
			super(Dialog, self).add_widget(widget)

	def on_content(self, instance, value):
		if self._container:
			self._container.clear_widgets()
			self._container.add_widget(value)

	def on__container(self, instance, value):
		if value is None or self.content is None:
			return
		self._container.clear_widgets()
		self._container.add_widget(self.content)

	def on_touch_down(self, touch):
		if self.disabled and self.collide_point(*touch.pos):
			return True
		return super(Dialog, self).on_touch_down(touch)

	def on__action_buttons(self, *args):
		self._action_area.clear_widgets()
		for btn in self._action_buttons:
			self._action_area.add_widget(btn)
