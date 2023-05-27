from kivy.graphics import Color
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
# from widgets.connection import ItemConfirm, Connection
# from widgets.drag_card import DragCard
from ui.widgets.project_card import ProjectCard

Builder.load_file('ui/screens/menu_screen.kv')


class MenuScreen(MDScreen):
    pass
