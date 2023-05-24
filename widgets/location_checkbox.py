from kivy.lang import Builder
from kivymd.uix.button import MDRectangleFlatIconButton


Builder.load_file('widgets/location_checkbox.kv')


class LocationCheckbox(MDRectangleFlatIconButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.marked: bool = False

    def on_press(self):
        if not self.marked:
            self.marked = True
            self.icon = "checkbox-marked"
        else:
            self.marked = False
            self.icon = "checkbox-blank-outline"
