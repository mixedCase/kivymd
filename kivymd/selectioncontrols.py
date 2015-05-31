# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, OptionProperty, ListProperty, BoundedNumericProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import AliasProperty, BooleanProperty
from kivy.metrics import dp
from layouts import MaterialGridLayout, MaterialBoxLayout
from kivymd.label import MaterialLabel
from ripplebehavior import RippleBehavior

from elevationbehaviour import ElevationBehaviour
from kivy.animation import Animation
from material_resources import get_rgba_color, get_btn_down_color
from theme import ThemeBehaviour

txt_chkbox_kv = '''
<MaterialTextCheckbox>:
	_label:		label
	_checkbox:	checkbox

	MaterialLabel:
		id:					label
		text:				root.text
		size_hint:			.8, 1
		font_style:			'Body1'
		theme_text_color:	'Primary'
		halign:				'left'
		valign:				'middle'

	MaterialToggleIcon:
		id: checkbox
		icon: 				'md-check-box-outline-blank'
		size_hint: 			.2, 1

'''

class MaterialTextCheckBox(ThemeBehaviour, RippleBehavior, MaterialGridLayout):

	text = StringProperty()

	active = BooleanProperty(False)

	_label = ObjectProperty()
	_checkbox = ObjectProperty()
	def __init__(self, **kwargs):
		# self._label = MaterialLabel(size_hint=(.8, 1),
		# 							font_style='Body1',
		# 							theme_text_color='Primary',
		# 							halign='left',
		# 							valign='middle')
		# self._checkbox = MaterialToggleIcon(icon='md-check-box-outline-blank')
		Builder.load_string(txt_chkbox_kv)
		super(MaterialTextCheckBox, self).__init__(**kwargs)
		self.register_event_type('on_active')
		self.cols = 2
		self._checkbox.bind(on_active=lambda *x: self.dispatch('on_active'))
		# self.add_widget(self._label)
		# self.add_widget(self._checkbox)

	def on_active(self):
		self.active = self._checkbox.active
