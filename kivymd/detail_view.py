# -*- coding: utf-8 -*-
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView

from layouts import MaterialBoxLayout
from kivymd.label import MaterialLabel
from list import List


class DetailView(ModalView):
    """ModalView similar to those seen used for showing contact details on
    MD apps.
    """

    def __init__(self, **kwargs):
        self._layout = MaterialBoxLayout
        self._title_layout = RelativeLayout()
        self._title_header = MaterialLabel()
        self._title_bg = Image()
        self._list = List()
        super(DetailView, self).__init__(**kwargs)
        self._layout.add_widget(self._title_layout)
        self._layout.add_widget(self.list)
