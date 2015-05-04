# -*- coding: utf-8 -*-
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.modalview import ModalView
from twisted.internet import defer

from layouts import MaterialBoxLayout as BoxLayout
from layouts import MaterialAnchorLayout as AnchorLayout
from kivymd.label import MaterialLabel as Label


class DeferredModalView(ModalView):
    def __init__(self, **kwargs):
        super(DeferredModalView, self).__init__(**kwargs)
        self.d = None

    def open(self, *largs):
        self.d = defer.Deferred()
        super(DeferredModalView, self).open(*largs)
        return self.d

    def dismiss(self, return_value=None, *largs, **kwargs):
        self.d.callback(return_value)
        super(DeferredModalView, self).dismiss(*largs, **kwargs)


class BlankPopup(DeferredModalView):
    content = ObjectProperty(None)
    _container = BoxLayout()

    def __init__(self, **kwargs):
        self.background_color = (0, 0, 0, 0.7)
        super(BlankPopup, self).__init__(**kwargs)
        self.bl = BoxLayout(orientation="vertical")
        self.anchor_y = "top"
        self.padding = 7
        self.bl.add_widget(self._container)
        self.add_widget(self.bl)

    def on_content(self, instance, value):
        self._container.clear_widgets()
        self._container.add_widget(value)


class TitledPopup(BlankPopup):
    title = StringProperty("Title")

    def __init__(self, **kwargs):
        super(TitledPopup, self).__init__(**kwargs)
        al_title = AnchorLayout(anchor_x="left",
                                height=40,
                                size_hint=(1, None))
        al_title.add_widget(Label(text=self.title))
        self.bl.clear_widgets()
        self.bl.add_widget(al_title)
        self.bl.add_widget(self._container)
