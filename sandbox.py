from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout

from ui.widgets.interactions_content import InteractionsContent
from ui.assets_loader import prepare_assets

KV = '''
Screen:
    ScrollView:
        do_scroll_x: False
        id: scroll_interactions
        pos_hint: {"x": 0.2, "y": 0}
        size_hint: 0.9, 1

        InteractionsContent:
            pos_hint: {"center_x": 0.5}
            size_hint: 0.8, None
            height: self.minimum_height

'''


class ScrollableImageApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.theme_style = "Dark"

        prepare_assets()
        return Builder.load_string(KV)


ScrollableImageApp().run()
