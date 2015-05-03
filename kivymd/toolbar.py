# -*- coding: utf-8 -*-
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout as _BoxLayout
from kivy.metrics import dp

from kivymd import material_resources as m_res
from layouts import MaterialRelativeLayout
from label import MaterialLabel
from button import MaterialIcon


class Toolbar(MaterialRelativeLayout):
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

	nav_button = ListProperty()
	"""Button left of the title, value must be a list with icon char and
	 callback

	If the icon (first value) is set to None the button will be hidden.

	Example:
		("\xf00c", self.my_callback_method)
	"""

	def __init__(self, **kwargs):
		self._lbl_title = MaterialLabel(style="bold",
		                                text=self.title,
		                                pos=(dp(24),0))
		super(Toolbar, self).__init__(**kwargs)
		self.size_hint_y = None
		self.height = dp(48)
		self.spacing = dp(1)
		self.background_color = (0, 0.5882352941176471, 0.5333333333333333, 1)

		self._nav_button = MaterialIcon(size_hint_x=None,
		                                size=(0,dp(48)),
		                                pos=(dp(12),0))

		self._bl_action_buttons = _BoxLayout(size_hint_x=None, width=0)
		self._action_buttons = []

		self.add_widget(self._nav_button)
		self.add_widget(self._lbl_title)
		self.add_widget(self._bl_action_buttons)

		self.bind(width=lambda x, y: self._refresh_action_buttons())
		self.nav_button = ['', None]  # Setting a default in the ListProperty
		# somehow makes it bug, so we set it at the end of __init__

	def on_nav_button(self, instance, value):
		self._nav_button.icon = value[0]
		if value[0] == '':
			self._nav_button.width = 0
			self._lbl_title.x = dp(24)
		else:
			self._nav_button.width = dp(48)
			self._lbl_title.x = dp(72)
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
		button = MaterialIcon(size=(dp(48),dp(48)))
		button.icon = icon
		if action:
			button.bind(on_release=action)

		self._bl_action_buttons.width += dp(48)
		self._bl_action_buttons.x -= dp(48)
		self._bl_action_buttons.add_widget(button)
		self._action_buttons.append(button)
		self._refresh_action_buttons()

	def get_action_buttons(self):
		"""Returns all action buttons on the toolbar."""
		return self._action_buttons

	def delete_action_button(self, button_widget):
		"""Deletes from the toolbar the provided action button.

		:param button_widget: The action button instance.
		:type button_widget: MaterialIcon
		"""
		self._bl_action_buttons.remove_widget(button_widget)
		self._action_buttons.remove(button_widget)
		self._refresh_action_buttons()

	def clear_action_buttons(self):
		self._bl_action_buttons.clear_widgets()
		self._action_buttons = []
		self._refresh_action_buttons()

	def _refresh_action_buttons(self):
		self._bl_action_buttons.clear_widgets()
		self._bl_action_buttons.width = 0
		self._bl_action_buttons.x = self.width - dp(4)

		for i in self._action_buttons:
			self._bl_action_buttons.width += m_res.TOUCH_TARGET_HEIGHT
			self._bl_action_buttons.x -= m_res.TOUCH_TARGET_HEIGHT
			self._bl_action_buttons.add_widget(i)

	def on_title(self, instance, value):
		self._lbl_title.text = value
