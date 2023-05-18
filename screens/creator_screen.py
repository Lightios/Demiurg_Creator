from kivy.graphics import Color
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
# from widgets.connection import ItemConfirm, Connection
# from widgets.drag_card import DragCard
from widgets.button_location import ButtonLocation
from widgets.grid import Grid
from widgets.location import Location


Builder.load_file('screens/creator_screen.kv')


class CreatorScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.marked_card = None

