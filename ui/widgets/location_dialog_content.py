from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu

from ui.widgets.location_checkbox import LocationCheckbox

Builder.load_file('ui/widgets/location_dialog_content.kv')


# menu_items = [
#             {
#                 "text": "Edit",
#                 "viewclass": "OneLineListItem",
#                 # "on_release": self.menu_callback,
#             },
#             {
#                 "text": "Delete",
#                 "viewclass": "OneLineListItem",
#                 # "on_release": self.delete,
#             }
#
#         ]
#
#
# class LocationMenu( MDDropdownMenu ):
#     def __init__(self, location, **kwargs):
#         # background_color="white",
#         super().__init__(**kwargs)
#         self.caller = location
#         self.items = menu_items
#         self.width_mult = 3
#         self.max_height = dp(202)
#
#     def open_dialog(self):
#         dialog = MDDialog(
#             title="Edit location",
#             type="custom",
#             content_cls=Content(),
#             buttons=[
#                 MDFlatButton(
#                     text="CANCEL",
#                     theme_text_color="Custom",
#                     text_color=self.theme_cls.primary_color,
#                 ),
#                 MDFlatButton(
#                     text="OK",
#                     theme_text_color="Custom",
#                     text_color=self.theme_cls.primary_color,
#                 ),
#             ],
#         )
#


class LocationDialogContent(BoxLayout):
    def __init__(self, location, **kwargs):
        super().__init__(**kwargs)

        self.ids.name.text = location.name
        self.ids.description.text = location.description
        if location.is_start:
            self.ids.start.on_press()

        if location.is_end:
            self.ids.end.on_press()
