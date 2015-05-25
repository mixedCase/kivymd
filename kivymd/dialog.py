# -*- coding: utf-8 -*-

from kivy.properties import StringProperty, ObjectProperty, NumericProperty, BooleanProperty, ListProperty
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from layouts import MaterialGridLayout, MaterialBoxLayout, MaterialAnchorLayout, MaterialRelativeLayout
from kivymd.label import MaterialLabel
from kivymd.button import FlatButton
from kivymd.shadow import Shadow
from kivy.animation import Animation
from kivy.clock import Clock
from theme import ThemeBehaviour
from elevationbehaviour import ElevationBehaviour




class DialogException(Exception):
	'''Popup exception, fired when multiple content widgets are added to the
	popup.

	.. versionadded:: 1.4.0
	'''

class Dialog(ThemeBehaviour, ElevationBehaviour, MaterialBoxLayout):
	auto_dismiss = BooleanProperty(True)
	'''This property determines if the view is automatically
	dismissed when the user clicks outside it.

	:attr:`auto_dismiss` is a :class:`~kivy.properties.BooleanProperty` and
	defaults to True.
	'''

	attach_to = ObjectProperty(None)
	'''If a widget is set on attach_to, the view will attach to the nearest
	parent window of the widget. If none is found, it will attach to the
	main/global Window.

	:attr:`attach_to` is an :class:`~kivy.properties.ObjectProperty` and
	defaults to None.
	'''

	title = StringProperty('')

	content = ObjectProperty()


	_anim_alpha = NumericProperty(0)

	_anim_duration = NumericProperty(.1)

	_window = ObjectProperty(None, allownone=True)

	_action_buttons = ListProperty([])

	_container = ObjectProperty(None)
	__events__ = ('on_open', 'on_dismiss')

	def __init__(self, **kwargs):
		self.orientation = 'vertical'
		self._main_area = GridLayout()
		self._main_area.cols = 1
		self._main_area.padding = (dp(24), dp(24), dp(24), 0)
		self._main_area.spacing = dp(20)

		self._parent = None

		self._lbl_title = MaterialLabel(font_style='Title',
										theme_text_color='Primary',
										halign='left',
										valign='middle',
										size_hint=(1, None))

		self._container = AnchorLayout(anchor_y='top')

		self._action_area = AnchorLayout(anchor_x='right',
										 anchor_y='center',
										 size_hint=(1, None),
										 height=dp(48),
										 padding=(dp(8), dp(8)),
										 spacing=dp(4))

		self._action_btn_box = BoxLayout(size_hint_x=None,
										 width=0)

		self.shadow = Shadow(size_hint=(None, None),
							 opacity=0.5)

		super(Dialog, self).__init__(**kwargs)
		self.elevation = 12
		if self.auto_dismiss:
			self.shadow.bind(on_release=lambda x: self.dismiss())
		self.background_color = self._theme_cls.dialog_background_color
		self._lbl_title.theme_style = self._theme_cls.theme_style

		self._main_area.add_widget(self._lbl_title)
		self._main_area.add_widget(self._container)
		self._action_area.add_widget(self._action_btn_box)
		super(Dialog, self).add_widget(self._main_area)
		super(Dialog, self).add_widget(self._action_area)

		self.bind(on_pos=self._update_layout,
				  on_size=self._update_layout)


	def add_action_button(self, text, action=None):
		"""Add an :class:`FlatButton` to the right of the action area.

		:param icon: Unicode character for the icon
		:type icon: str or None
		:param action: Function set to trigger when on_release fires
		:type action: function or None
		"""
		button = FlatButton(text=text,
							text_color=self._theme_cls.primary_color,
							background_color=self.background_color,
							size_hint=(1, None),
							height=dp(36))
		if action:
			button.bind(on_release=action)
		self._action_buttons.append(button)

	def open(self, *largs):
		'''Show the view window from the :attr:`attach_to` widget. If set, it
		will attach to the nearest window. If the widget is not attached to any
		window, the view will attach to the global
		:class:`~kivy.core.window.Window`.
		'''
		if self._window is not None:
			return self
		# search window
		self._window = self._search_window()
		if not self._window:
			return self
		self.shadow.size = self._window.size
		self.shadow.fade_in(.2, add_to=self._window)
		self.shadow.bind(on_visible=lambda *x: self.dispatch('on_open'))
		self._window.add_widget(self)
		self._window.bind(
			on_resize=self._align_center,
			on_keyboard=self._handle_keyboard)
		self.center = self._window.center
		self.bind(size=self._update_center)

		self._update_layout()
		return self


	def dismiss(self, *largs, **kwargs):
		'''Close the view if it is open. If you really want to close the
		view, whatever the on_dismiss event returns, you can use the *force*
		argument:
		::

			view = ModalView(...)
			view.dismiss(force=True)

		When the view is dismissed, it will be faded out before being
		removed from the parent. If you don't want animation, use::

			view.dismiss(animation=False)

		'''
		if self._window is None:
			return self
		if self.dispatch('on_dismiss') is True:
			if kwargs.get('force', False) is not True:
				return self
		self.shadow.fade_out(.2)
		self.shadow.bind(on_invisible=self._real_remove_widget)
		return self

	def _update_layout(self, *args):
		self._lbl_title.text_size = (self._lbl_title.width, None )
		self._lbl_title.texture_update()
		self._lbl_title.height = max(self._lbl_title.texture_size[1], self.height / 4)

		self._action_btn_box.clear_widgets()
		self._action_btn_box.width = 0
		for btn in self._action_buttons:
			btn.width = min(len(btn.text) * sp(13), self.width / len(self._action_buttons))
			self._action_btn_box.width += btn.width
			if len(self._action_buttons) > 1:
				self._action_btn_box.width += dp(4)
			self._action_btn_box.add_widget(btn)


	def _search_window(self):
		# get window to attach to
		window = None
		if self.attach_to is not None:
			window = self.attach_to.get_parent_window()
			if not window:
				window = self.attach_to.get_root_window()
		if not window:
			from kivy.core.window import Window

			window = Window
		return window


	def _update_center(self, *args):
		if not self._window:
			return
		# XXX HACK DONT REMOVE OR FOUND AND FIX THE ISSUE
		# It seems that if we don't access to the center before assigning a new
		# value, no dispatch will be done >_>
		self.center = self._window.center


	def on_size(self, instance, value):
		self._align_center()

	def _align_center(self, *l):
		if self._window:
			self.center = self._window.center
			# hack to resize dark background on window resize
			_window = self._window
			self._window = None
			self._window = _window

	def on_touch_down(self, touch):
		if not self.collide_point(*touch.pos):
			if self.auto_dismiss:
				self.dismiss()
				return True
		super(Dialog, self).on_touch_down(touch)
		return True

	def on_touch_move(self, touch):
		super(Dialog, self).on_touch_move(touch)
		return True

	def on_touch_up(self, touch):
		super(Dialog, self).on_touch_up(touch)
		return True

	def on__anim_alpha(self, instance, value):
		if value == 0 and self._window is not None:
			self._real_remove_widget()

	def _real_remove_widget(self, *args):
		if self._window is None:
			return
		self._window.remove_widget(self)
		self._window.unbind(
			on_resize=self._align_center,
			on_keyboard=self._handle_keyboard)
		self._window = None

	def on_open(self):
		pass

	def on_dismiss(self):
		pass

	def _handle_keyboard(self, window, key, *largs):
		if key == 27 and self.auto_dismiss:
			self.dismiss()
			return True


	def on_title(self, instance, value):
		self._lbl_title.text = value

	def add_widget(self, widget):
		if len(self._container.children) > 0:
			self.content = widget
		else:
			super(Dialog, self).add_widget(widget)

	def on_content(self, instance, value):
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
