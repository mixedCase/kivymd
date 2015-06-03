# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.widget import Widget

avatar_kv = '''
<Avatar>:
	canvas:
		Color:
			rgba: 1, 1, 1, 1
		Ellipse:
			source: self.source
			size: self.size
			pos: self.pos

'''


class Avatar(Widget):

	source = StringProperty('')

	def __init__(self, **kwargs):
		Builder.load_string(avatar_kv)
		super(Avatar, self).__init__(**kwargs)