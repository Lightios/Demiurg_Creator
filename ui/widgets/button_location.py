from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDIconButton

Builder.load_file('ui/widgets/button_location.kv')


class ButtonLocation(MDIconButton):
    grid = ObjectProperty()

    def __init__(self, column=0, row=0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.column: int = column
        self.row: int = row




