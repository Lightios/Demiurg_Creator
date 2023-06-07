from kivy.graphics import Color
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from ui.widgets.button_location import ButtonLocation
from ui.widgets.grid import Grid
from ui.widgets.location import Location
from ui.widgets.interactions_content import InteractionsContent


Builder.load_file('ui/screens/creator_screen.kv')


class CreatorScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def show_grid(self):
        self.ids.scroll_grid.pos_hint = {"x": 0.1, "y": 0}
        self.ids.scroll_interactions.pos_hint = {"x": -10, "y": -10}

    def show_interactions_content(self):
        self.ids.scroll_grid.pos_hint = {"x": -10, "y": -10}
        self.ids.scroll_interactions.pos_hint = {"x": 0.2, "y": -0.02}

