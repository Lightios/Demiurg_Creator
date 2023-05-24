from kivy.core.text import LabelBase
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.card import MDCard
from kivy.config import Config

from screens.menu_screen import MenuScreen
from screens.creator_screen import CreatorScreen


class ContentNavigationDrawer(RelativeLayout):
    pass


class DemiurgApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.theme_style = "Dark"


class NavigationButton(MDCard):
    text = StringProperty()


LabelBase.register(name='Monoton', fn_regular='./assets/Monoton-Regular.ttf')
LabelBase.register(name='Nunito', fn_regular='./assets/Nunito-VariableFont_wght.ttf')
LabelBase.register(name='Nunito_bold', fn_regular='./assets/Nunito-Bold.ttf')

Window.size = (1400, 800)
Window.top = 10
Window.left = 10


Config.set('input', 'mouse', 'mouse,disable_multitouch')

DemiurgApp().run()
