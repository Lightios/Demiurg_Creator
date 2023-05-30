from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from typing import Dict
from uuid import uuid4, UUID
from kivymd.toast import toast

from ui.widgets.connection import Connection
from ui.widgets.location_dialog_content import LocationDialogContent

Builder.load_file('ui/widgets/location.kv')


class Location(MDCard):
    image_sources = [
        "ui/assets/locations/start_end_location_shape.png",
        "ui/assets/locations/start_location_shape.png",
        "ui/assets/locations/end_location_shape.png",
        "ui/assets/locations/location_shape.png",
    ]

    background_image = StringProperty()
    description: str = ""
    dialog: MDDialog | None = None
    exits: Dict  # [str, Location | None]
    exit_descriptions: Dict[str, str]
    location_id: UUID  # can't be called "id" because it's reserved by Kivy
    is_start: bool = False
    is_end: bool = False
    name = StringProperty("New Location")

    row: int
    column: int

    def __init__(self, button, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.column = button.column
        self.row = button.row
        self.exits = {"N": None, "E": None, "S": None, "W": None}
        self.exit_descriptions = {"N": "", "E": "", "S": "", "W": ""}
        self.location_id = uuid4()

    def on_touch_down(self, touch):
        if touch.button == "right":
            if self.collide_point(*touch.pos):
                self.dialog = MDDialog(
                    title="Edit location",
                    type="custom",
                    content_cls=LocationDialogContent(self),
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            theme_text_color="Custom",
                            text_color=self.theme_cls.primary_color,
                            on_press=lambda x: self.dialog.dismiss(),
                        ),
                        MDFlatButton(
                            text="OK",
                            theme_text_color="Custom",
                            text_color=self.theme_cls.primary_color,
                            on_press=lambda x: self.confirm(),
                        ),
                    ],
                )
                self.dialog.open()

    def delete(self):
        self.parent.delete_location(self)
        self.dialog.dismiss()

    def confirm(self):
        can_proceed = self.check_start()

        if not can_proceed:
            return

        self.is_end = self.dialog.content_cls.ids.end.marked
        self.name = self.dialog.content_cls.ids.name.text
        self.description = self.dialog.content_cls.ids.description.text

        for card in self.dialog.content_cls.ids.stack.children:
            description = card.ids.text_field.text
            self.exit_descriptions[card.direction] = description

        self.dialog.dismiss()
        self.ids.label.text = self.name

        if self.is_start and self.is_end:
            self.ids.background_image.source = Location.image_sources[0]
        elif self.is_start:
            self.ids.background_image.source = Location.image_sources[1]
        elif self.is_end:
            self.ids.background_image.source = Location.image_sources[2]
        else:
            self.ids.background_image.source = Location.image_sources[3]

    def check_start(self):
        # trying to mark as new start location
        if self.dialog.content_cls.ids.start.marked and not self.is_start:
            if self.parent.start_location is None:
                self.is_start = self.dialog.content_cls.ids.start.marked
                self.parent.start_location = self
                return True
            else:
                toast("Can't set more than one start location")
                return False

        # unmarking
        if not self.dialog.content_cls.ids.start.marked and self.is_start:
            self.parent.start_location = None
            self.is_start = False
            return True

        # didn't do anything
        return True
