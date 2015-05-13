# -*- coding: utf-8 -*-
import kivy
import kivymd

kivy.require('1.9.0')

from kivy.app import App
from kivy.metrics import dp
from kivymd.layouts import MaterialRelativeLayout
from kivymd.toolbar import Toolbar
from kivymd.navigationdrawer import NavigationDrawer, NavigationDrawerButton, \
	NavigationDrawerCategory
from kivymd.button import RaisedButton
from kivymd.label import MaterialLabel
from kivymd.theme import ThemeBehaviour, ThemeManager


class MainWidget(ThemeBehaviour, MaterialRelativeLayout):
	def __init__(self, **kwargs):
		self.toolbar = Toolbar(title="KivyMD Kitchen Sink",
							   auto_color=False,
							   color_style='Dark')
		self.nav = NavigationDrawer(
			side="left",
			header_img=kivymd.images_path + "PLACEHOLDER_BG.jpg",
			width=dp(400))
		super(MainWidget, self).__init__(**kwargs)

		self.background_color = self._theme_cls.main_background_color

		self.toolbar.nav_button = ["md-view-headline", lambda: self.nav.toggle()]
		# self.toolbar.add_action_button("md-view-headline")


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
		self.r_btn_1 = RaisedButton(text="Raised btn",
									 size_hint=(None, None),
									 size=(dp(100), dp(36)),
									 pos_hint=({'center_x': 0.3, 'center_y': 0.5}),
									 elevation_normal=2,
									 auto_color=True,
									 color_style='Dark')
		self.r_lbl_1 = MaterialLabel(text="Elevation:\n{:d}".format(int(self.r_btn_1._elevation)),
									 font_style='Body1',
									 auto_color=False,
									 width=dp(100),
									 halign='center',
									 pos_hint=({'center_x': 0.3, 'center_y': 0.4}))

		self.r_btn_1.bind(_elevation=lambda *x: setattr(self.r_lbl_1, 'text', "Elevation:\n{:d}".format(int(self.r_btn_1._elevation))))
		self.add_widget(self.r_btn_1)
		self.add_widget(self.r_lbl_1)
		self.r_btn_2 = RaisedButton(text="Raised btn",
									 size_hint=(None, None),
									 size=(dp(100), dp(36)),
									 pos_hint=({'center_x': 0.7, 'center_y': 0.5}),
									 elevation_normal=6,
									 auto_color=False,
									 color_style='Dark',
									 disabled=False)
		self.r_lbl_2 = MaterialLabel(text="Elevation:\n{:d}".format(int(self.r_btn_2._elevation)),
									 font_style='Body1',
									 auto_color=True,
									 width=dp(100),
									 halign='center',
									 pos_hint=({'center_x': 0.7, 'center_y': 0.4}))

		self.r_btn_2.bind(_elevation=lambda *x: setattr(self.r_lbl_2, 'text', "Elevation:\n{:d}".format(int(self.r_btn_2._elevation))))
		self.add_widget(self.r_btn_2)
		self.add_widget(self.r_lbl_2)


		self.add_widget(self.toolbar)
		self.add_widget(self.nav)



	def on_width(self, instance, value):
		self.toolbar.width = value

	def on_height(self, instance, value):
		self.toolbar.y = self.height - self.toolbar.height


class KitchenSink(App):
	theme_cls = ThemeManager()

	def __init__(self, **kwargs):
		super(KitchenSink, self).__init__(**kwargs)
		self.theme_cls.primary_palette = 'BlueGrey'
		self.theme_cls.accent_palette = 'Teal'
		self.theme_cls.theme_style = 'Light'

	def on_start(self):
		pass

	def build(self):
		return MainWidget()

	def on_pause(self):
		return True

	def on_stop(self):
		pass


if __name__ == '__main__':
	KitchenSink().run()