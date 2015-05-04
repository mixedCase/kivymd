# -*- coding: utf-8 -*-
import kivy
import kivymd

kivy.require('1.9.0')

from kivy.app import App
from kivy.metrics import dp
from kivymd.layouts import MaterialRelativeLayout
from kivymd.toolbar import Toolbar
from kivymd.navigationdrawer import NavigationDrawer, NavigationDrawerButton, NavigationDrawerCategory
from kivymd.popup import TitledPopup
from kivymd.theme import ThemeManager


class MainWidget(MaterialRelativeLayout):
    def __init__(self, **kwargs):
        self.theme_manager = ThemeManager()
        self.toolbar = Toolbar(title="KivyMD Kitchen Sink App")
        self.nav = NavigationDrawer(
            side="left",
            header_img=kivymd.images_path + "PLACEHOLDER_BG.jpg",
            width=dp(400))
        super(MainWidget, self).__init__(**kwargs)

        self.background_color = (1, 1, 1, 1)

        self.popup = TitledPopup(title="Testar Popupen",
                                 size_hint=(None, None),
                                 size=('300dp', '100dp'))

        self.toolbar.nav_button = ["", lambda: self.nav.toggle()]
        self.toolbar.add_action_button("")
        self.toolbar.add_action_button("")
        self.toolbar.add_action_button("")
        self.toolbar.add_action_button("", action=lambda *x: self.popup.open())

        self.cat1 = NavigationDrawerCategory(subheader=False)
        self.cat_vendedores = NavigationDrawerCategory(text="Category 1")
        self.cat1.add_widget(NavigationDrawerButton(text="Button 1"))
        self.cat1.add_widget(NavigationDrawerButton(text="Button 2"))
        self.cat1.add_widget(NavigationDrawerButton(text="Button 3"))
        self.cat1.add_widget(NavigationDrawerButton(text="Button 4"))
        self.cat_vendedores.add_widget(NavigationDrawerButton(text="Button A"))
        self.cat_vendedores.add_widget(NavigationDrawerButton(text="Button B"))
        self.cat_vendedores.add_widget(NavigationDrawerButton(text="Button C"))
        self.nav.add_widget(self.cat1)
        self.nav.add_widget(self.cat_vendedores)



        self.add_widget(self.toolbar)
        self.add_widget(self.nav)

    def on_width(self, instance, value):
        self.toolbar.width = value

    def on_height(self, instance, value):
        self.toolbar.y = self.height - self.toolbar.height


class KitchenSink(App):
    def __init__(self, **kwargs):
        super(KitchenSink, self).__init__(**kwargs)

    def build(self):
        return MainWidget()

    def on_pause(self):
        return True

    def on_stop(self):
        pass


if __name__ == '__main__':
    KitchenSink().run()