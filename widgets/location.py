from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu

Builder.load_file('widgets/location.kv')

from widgets.location_dialog_content import LocationDialogContent


class Location(MDCard):
    image_sources = [
        "assets/locations/start_end_location_shape.png",
        "assets/locations/start_location_shape.png",
        "assets/locations/end_location_shape.png",
        "assets/locations/location_shape.png",
    ]

    background_image = StringProperty()
    name = StringProperty("New Location")
    description: str = ""
    is_start: bool = False
    is_end: bool = False
    column: int
    row: int

    def __init__(self, button, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.column = button.column
        self.row = button.row
        self.dialog: MDDialog | None = None

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
        print(1234)

    def confirm(self):
        self.name = self.dialog.content_cls.ids.name.text
        self.description = self.dialog.content_cls.ids.description.text

        self.is_start = self.dialog.content_cls.ids.start.marked
        self.is_end = self.dialog.content_cls.ids.end.marked

        self.dialog.dismiss()

        self.ids.label.text = self.name

        if self.is_start and self.is_end:
            self.ids.background_image.source = self.image_sources[0]
        elif self.is_start:
            self.ids.background_image.source = self.image_sources[1]
        elif self.is_end:
            self.ids.background_image.source = self.image_sources[2]
        else:
            self.ids.background_image.source = self.image_sources[3]


