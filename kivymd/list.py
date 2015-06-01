# -*- coding: utf-8 -*-

from kivy.lang import Builder

from kivy.adapters.listadapter import ListAdapter
from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.listview import CompositeListItem, ListItemButton, ListView, SelectableView
from kivy.properties import (OptionProperty, BoundedNumericProperty,
							 NumericProperty, ListProperty, StringProperty,
							 ObjectProperty, AliasProperty, BooleanProperty,
							 DictProperty)
from kivy.metrics import dp
from kivy.uix.behaviors import ToggleButtonBehavior, ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock
from kivy.uix.widget import Widget
from label import MaterialLabel
from ripplebehavior import RippleBehavior
from theme import ThemeBehaviour
from material_resources import get_rgba_color
from kivymd import images_path
from avatar import Avatar


materiallist_kv = '''
<MaterialList>:
	canvas:
		Clear
		Color:
			rgba: self._theme_cls.divider_color()
		Line:
			points: self.x, self.top, self.x + self.width, self.top
		Color:
			rgba: self.background_color

		Rectangle:
			size: self.size
			pos: self.pos

	_list_view:			list_view
	padding:			0, dp(8), 0, 0
	spacing:			dp(16)
	orientation:		'vertical'
	MaterialLabel:
		text:				root.title
		font_style:			'Body2'
		theme_text_color:	'Secondary'
		text_size:			self.size
		size_hint_y:		None
		height:				self.texture_size[1]
		padding_x:			dp(16)
	GridLayout:
		cols:			1
		ListView:
			id:				list_view

'''

Builder.load_string(materiallist_kv)

class MaterialList(ThemeBehaviour, BoxLayout):

	title = StringProperty('')

	tile_rows = BoundedNumericProperty(1, min=1, max=3)

	list_type = OptionProperty('text', options=('text', 'icon_text', 'avatar_text', 'avatar_text_icon'))

	text_color = ListProperty()

	text_color_selected = ListProperty()

	background_color_selected = ListProperty()

	background_color_disabled = ListProperty()

	divider_color = ListProperty([1, 1, 1, 0])

	selection_mode = OptionProperty('single', options=('none', 'single', 'multiple'))

	allow_empty_selection = BooleanProperty(False)

	selection_limit = NumericProperty(-1)

	list_data = ListProperty()

	selection = ListProperty([])

	_tile_height = NumericProperty(dp(48))
	_list_view = ObjectProperty()
	def __init__(self, **kwargs):
		super(MaterialList, self).__init__(**kwargs)
		self.register_event_type('on_selection')
		self.text_color = self._theme_cls.primary_text_color()
		self.text_color_selected = self._theme_cls.accent_color
		self.background_color_selected = get_rgba_color([self._theme_cls.theme_style, 'FlatButtonDown'])
		self.background_color_disabled = self._theme_cls.disabled_bg_color()

		self.bind(tile_rows=self._set_tile_height,
				  list_data=self._get_adapter)

	def on_selection(self, *args):
		pass

	def _get_adapter(self, *args):
		if self.list_type == 'text':
			converter = lambda row_index, rec: {'text': rec['text'],
												'secondary_text': rec['secondary_text'] if 'secondary_text' in rec else '',
												'tile_rows': self.tile_rows,
												'text_color_selected': self.text_color_selected,
												'background_color_selected': self.background_color_selected,
												'background_color_disabled': self.background_color_disabled,
												'divider_color': self.divider_color,
												'size_hint_y': None,
												'height': self._tile_height,
												'callback': rec['callback'] if 'callback' in rec else None}
			adapter = ListAdapter(data=self.list_data,
								  args_converter=converter,
								  cls=TextTile)
			adapter.bind(selection=self.setter('selection'))
			self._list_view.adapter = adapter
			self._list_view.adapter.selection_mode = self.selection_mode
			self._list_view.adapter.selection_limit = self.selection_limit
			self._list_view.adapter.allow_empty_selection = self.allow_empty_selection

		if self.list_type == 'icon_text':
			converter = lambda row_index, rec: {'icon': rec['icon'],
												'text': rec['text'],
												'secondary_text': rec['secondary_text'] if 'secondary_text' in rec else '',
												'tile_rows': self.tile_rows,
												'text_color_selected': self.text_color_selected,
												'background_color_selected': self.background_color_selected,
												'background_color_disabled': self.background_color_disabled,
												'divider_color': self.divider_color,
												'size_hint_y': None,
												'height': self._tile_height,
												'callback': rec['callback'] if 'callback' in rec else None}

			adapter = ListAdapter(data=self.list_data,
								  args_converter=converter,
								  cls=IconTextTile)
			adapter.bind(selection=self.setter('selection'))
			self._list_view.adapter = adapter
			self._list_view.adapter.selection_mode = self.selection_mode
			self._list_view.adapter.selection_limit = self.selection_limit
			self._list_view.adapter.allow_empty_selection = self.allow_empty_selection
		if self.list_type == 'avatar_text':
			converter = lambda row_index, rec: {'avatar': rec['avatar'],
												'text': rec['text'],
												'secondary_text': rec['secondary_text'] if 'secondary_text' in rec else '',
												'tile_rows': self.tile_rows,
												'text_color_selected': self.text_color_selected,
												'background_color_selected': self.background_color_selected,
												'background_color_disabled': self.background_color_disabled,
												'divider_color': self.divider_color,
												'size_hint_y': None,
												'height': self._tile_height,
												'callback': rec['callback'] if 'callback' in rec else None}

			adapter = ListAdapter(data=self.list_data,
								  args_converter=converter,
								  cls=AvatarTextTile)
			adapter.bind(selection=self.setter('selection'))
			self._list_view.adapter = adapter
			self._list_view.adapter.selection_mode = self.selection_mode
			self._list_view.adapter.selection_limit = self.selection_limit
			self._list_view.adapter.allow_empty_selection = self.allow_empty_selection



	def _set_tile_height(self, *args):
		if self.tile_rows == 1:
			if self.tile_type == 'text' or self.tile_type == 'icon_text':
				self._tile_height = dp(48)
			else:
				self._tile_height = dp(56)
		elif self.tile_rows == 2:
			self._tile_height = dp(72)
		else:
			self._tile_height = dp(88)



texttile_kv = '''
<TextTile>:
	canvas:
		Clear
		Color:
			rgba: self.background_color_disabled if self.disabled else \
			(self.background_color_selected if self.is_selected else self.background_color)
		Rectangle:
			size: self.size
			pos: self.pos
		Color:
			rgba: self.divider_color
		Line:
			points: self.x, self.y, self.x + self.width, self.y
			width: 1

	padding:		dp(16), 0
	anchor_x:		'center'
	anchor_y:		'center'

	GridLayout:
		cols:			1
		spacing:		dp(4)
		MaterialLabel:
			id: 				primary_label
			text:				root.text
			font_style:			'Subhead'
			theme_text_color:	'Primary'
			theme_style:		'Custom'
			text_color:			root._text_color if not root.is_selected else root.text_color_selected
			text_size:			self.size
			halign:				'left'
			valign:				'bottom' if len(root.secondary_text) > 1 else 'middle'

		MaterialLabel:
			id: 				secondary_label
			text:				root.secondary_text
			font_style:			'Body1'
			theme_text_color:	'Secondary'
			theme_style:		root._theme_cls.theme_style
			size_hint_y:		None if self.text == '' else 1
			text_size:			(self.width, None if self.text == '' else self.height)
			height:				self.texture_size[1]
			halign:				'left'
			valign:				'top'
'''
Builder.load_string(texttile_kv)

class TextTile(ThemeBehaviour, RippleBehavior, ButtonBehavior, AnchorLayout):

	text_color_selected = ListProperty()

	background_color_selected = ListProperty()

	background_color_disabled = ListProperty()

	divider_color = ListProperty()

	text = StringProperty('')
	secondary_text = StringProperty('')

	is_selected = BooleanProperty(False)

	callback = ObjectProperty()

	tile_rows = NumericProperty(1)

	index = NumericProperty(-1)

	_text_color = ListProperty([])
	def __init__(self, **kwargs):
		super(TextTile, self).__init__(**kwargs)
		self._text_color = self._theme_cls.primary_text_color()

	def select(self, *args):
		self.background_color = self.background_color_selected
		self._text_color = self.text_color_selected
		self.is_selected = True
		if isinstance(self.parent, CompositeListItem):
			self.parent.select_from_child(self, *args)

	def deselect(self, *args):
		self.background_color = (1, 1, 1, 0)
		self._text_color = self._theme_cls.primary_text_color()
		self.is_selected = False
		if isinstance(self.parent, CompositeListItem):
			self.parent.deselect_from_child(self, *args)

	def select_from_composite(self, *args):
		self.background_color = self.background_color_selected
		self._text_color = self.text_color_selected

	def deselect_from_composite(self, *args):
		self.background_color = (1, 1, 1, 0)
		self._text_color = self._theme_cls.primary_text_color()

	def on_is_selected(self, *args):
		if self.is_selected and self.callback:
			self.callback()


icontexttile_kv = '''
<IconTextTile>:
	canvas:
		Clear
		Color:
			rgba: self.background_color_disabled if self.disabled else \
			(self.background_color_selected if self.is_selected else self.background_color)
		Rectangle:
			size: self.size
			pos: self.pos
		Color:
			rgba: self.divider_color
		Line:
			points: self.x + dp(72), self.y, self.x + self.width, self.y
			width: 1

	anchor_x:			'center'
	anchor_y:			'center'
	padding:			dp(16), 0

	GridLayout:
		cols:			2
		AnchorLayout:
			anchor_x:		'left'
			anchor_y:		'center'
			size_hint:		None, 1
			width:			dp(56)
			MaterialLabel:
				id: 				icon_label
				icon:				root.icon
				font_style:			'Icon'
				theme_text_color:	'Secondary'
				theme_style:		'Custom'
				text_color:			root._icon_color
				text_size:			self.size
				size_hint:			None, None
				size:				dp(24), dp(24)

		GridLayout:
			cols:			1
			spacing:		dp(4)
			MaterialLabel:
				id: primary_label
				text:				root.text
				font_style:			'Subhead'
				theme_text_color:	'Primary'
				theme_style:		'Custom'
				text_color:			root._text_color if not root.is_selected else root.text_color_selected
				text_size:			self.size
				halign:				'left'
				valign:				'bottom'

			MaterialLabel:
				id: secondary_label
				text:				root.secondary_text
				font_style:			'Body1'
				theme_text_color:	'Secondary'
				theme_style:		root._theme_cls.theme_style
				text_size:			self.size
				halign:				'left'
				valign:				'top'
'''
Builder.load_string(icontexttile_kv)

class IconTextTile(ThemeBehaviour, RippleBehavior, ButtonBehavior, AnchorLayout):

	text_color_selected = ListProperty()

	background_color_selected = ListProperty()

	background_color_disabled = ListProperty()

	divider_color = ListProperty()

	icon = StringProperty('')
	text = StringProperty('')
	secondary_text = StringProperty('')

	is_selected = BooleanProperty(False)

	callback = ObjectProperty()

	tile_rows = NumericProperty(1)

	index = NumericProperty(-1)

	_text_color = ListProperty([])
	_icon_color = ListProperty([])
	def __init__(self, **kwargs):
		super(IconTextTile, self).__init__(**kwargs)
		self._text_color = self._theme_cls.primary_text_color()
		self._icon_color = self._theme_cls.secondary_text_color()

	def select(self, *args):
		self.background_color = self.background_color_selected
		self._text_color = self.text_color_selected
		self._icon_color = self.text_color_selected
		self.is_selected = True
		if isinstance(self.parent, CompositeListItem):
			self.parent.select_from_child(self, *args)

	def deselect(self, *args):
		self.background_color = (1, 1, 1, 0)
		self._text_color = self._theme_cls.primary_text_color()
		self._icon_color = self._theme_cls.secondary_text_color()
		self.is_selected = False
		if isinstance(self.parent, CompositeListItem):
			self.parent.deselect_from_child(self, *args)

	def select_from_composite(self, *args):
		self.background_color = self.background_color_selected
		self._text_color = self.text_color_selected
		self._icon_color = self.text_color_selected

	def deselect_from_composite(self, *args):
		self.background_color = (1, 1, 1, 0)
		self._text_color = self._theme_cls.primary_text_color()
		self._icon_color = self._theme_cls.secondary_text_color()

	def on_is_selected(self, *args):
		if self.is_selected and self.callback:
			self.callback()

avatartexttile_kv = '''
<AvatarTextTile>:
	canvas:
		Clear
		Color:
			rgba: self.background_color_disabled if self.disabled else \
			(self.background_color_selected if self.is_selected else self.background_color)
		Rectangle:
			size: self.size
			pos: self.pos
		Color:
			rgba: self.divider_color
		Line:
			points: self.x + dp(72), self.y, self.x + self.width, self.y
			width: 1

	anchor_x:			'center'
	anchor_y:			'center'
	padding:			dp(16), 0

	GridLayout:
		cols:			2
		AnchorLayout:
			anchor_x:		'left'
			anchor_y:		'center'
			size_hint:		None, 1
			width:			dp(56)
			Avatar:
				id: 				avatar
				source:				root.avatar
				size_hint:			None, None
				size:				dp(36), dp(36)

		GridLayout:
			cols:			1
			spacing:		dp(4)
			MaterialLabel:
				id: primary_label
				text:				root.text
				font_style:			'Subhead'
				theme_text_color:	'Primary'
				theme_style:		'Custom'
				text_color:			root._text_color if not root.is_selected else root.text_color_selected
				text_size:			self.size
				halign:				'left'
				valign:				'bottom'

			MaterialLabel:
				id: secondary_label
				text:				root.secondary_text
				font_style:			'Body1'
				theme_text_color:	'Secondary'
				theme_style:		root._theme_cls.theme_style
				text_size:			self.size
				halign:				'left'
				valign:				'top'
'''

Builder.load_string(avatartexttile_kv)


class AvatarTextTile(ThemeBehaviour, RippleBehavior, ButtonBehavior, AnchorLayout):

	text_color_selected = ListProperty()

	background_color_selected = ListProperty()

	background_color_disabled = ListProperty()

	divider_color = ListProperty()

	avatar = StringProperty('')
	text = StringProperty('')
	secondary_text = StringProperty('')

	is_selected = BooleanProperty(False)

	callback = ObjectProperty()

	tile_rows = NumericProperty(1)

	index = NumericProperty(-1)

	_text_color = ListProperty([])
	def __init__(self, **kwargs):
		super(AvatarTextTile, self).__init__(**kwargs)
		self._text_color = self._theme_cls.primary_text_color()

	def select(self, *args):
		self.background_color = self.background_color_selected
		self._text_color = self.text_color_selected
		self.is_selected = True
		if isinstance(self.parent, CompositeListItem):
			self.parent.select_from_child(self, *args)

	def deselect(self, *args):
		self.background_color = (1, 1, 1, 0)
		self._text_color = self._theme_cls.primary_text_color()
		self.is_selected = False
		if isinstance(self.parent, CompositeListItem):
			self.parent.deselect_from_child(self, *args)

	def select_from_composite(self, *args):
		self.background_color = self.background_color_selected
		self._text_color = self.text_color_selected

	def deselect_from_composite(self, *args):
		self.background_color = (1, 1, 1, 0)
		self._text_color = self._theme_cls.primary_text_color()

	def on_is_selected(self, *args):
		if self.is_selected and self.callback:
			self.callback()
