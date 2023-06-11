from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.card import MDCard


Builder.load_file('ui/widgets/oldschool_button.kv')


class OldschoolButton(MDCard):
    name = StringProperty()
    source = StringProperty()

    def on_kv_post(self, base_widget):
        self.source = f"ui/assets/buttons/{self.name}.png"

    #
    # def resize(self):
    #     button = self.ids.button
    #     image = self.ids.image
    #
    #     button.size = image.texture_size
