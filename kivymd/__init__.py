# -*- coding: utf-8 -*-
import os
from kivy.lang import Builder

Builder.load_string("""
<SlidingModal>:
	canvas:
		Color:
			rgba: (0,0,0,self._anim_alpha)
		Rectangle:
			size: self._window.size if self._window else (0, 0)
			pos: (0, 0)
""")

path = os.path.dirname(__file__)
images_path = os.path.join(path, "images/")
fonts_path = os.path.join(path, "fonts/")