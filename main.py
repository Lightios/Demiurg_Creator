from kivymd.app import MDApp
from kivy.core.window import Window

from screens.creator_screen import CreatorScreen

class DemiurgApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.theme_style = "Dark"


Window.size = (1400, 800)
Window.top = 10
Window.left = 10

DemiurgApp().run()
