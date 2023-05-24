from kivy.lang import Builder
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard

Builder.load_file('widgets/connection.kv')


class Connection(MDCard):
    def __init__(self, direction: tuple, source, destination, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source = source
        self.destination = destination

        # determines on which side of location it was created
        if direction == (1, 0) or direction == (-1, 0):
            first = "right"
            second = "left"
            self.height = source.height

            if direction == (1, 0):
                self.pos[0] += source.width
        else:
            first = "up"
            second = "down"
            self.width = source.height

            if direction == (0, -1):
                self.pos[1] += source.height

        self.ids.first.icon = f"chevron-{first}"
        self.ids.second.icon = f"chevron-{second}"

