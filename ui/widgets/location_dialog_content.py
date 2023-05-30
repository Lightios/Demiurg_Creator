from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard

from ui.widgets.location_checkbox import LocationCheckbox

Builder.load_file('ui/widgets/location_dialog_content.kv')


def letter_to_full_direction(letter: str):
    return {"N": "North", "E": "East", "S": "South", "W": "West"}[letter]


class LocationDialogContent(BoxLayout):
    def __init__(self, location, **kwargs):
        super().__init__(**kwargs)

        self.ids.name.text = location.name
        self.ids.description.text = location.description
        self.location = location

        if location.is_start:
            self.ids.start.on_press()

        if location.is_end:
            self.ids.end.on_press()

        for key, value in location.exits.items():
            if value is not None:
                exit_card = ExitCard(direction=key)
                self.ids.stack.add_widget(exit_card)


class ExitCard(MDCard):
    direction: str
    text = StringProperty()

    def __init__(self, direction, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.direction = direction
        self.text = letter_to_full_direction(direction)

