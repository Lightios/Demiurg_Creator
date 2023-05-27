from kivy.graphics import Color
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from ui.widgets.button_location import ButtonLocation
from ui.widgets.grid import Grid
from ui.widgets.location import Location


Builder.load_file('ui/screens/creator_screen.kv')


class CreatorScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.marked_card = None

