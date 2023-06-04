from kivy.lang import Builder
from kivy.properties import ColorProperty, ObjectProperty
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard

Builder.load_file('ui/widgets/connection.kv')


class Connection(MDCard):

    def __init__(self, direction: str, source, destination, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source = source
        self.destination = destination
        self.direction = direction

        if direction == "right" or direction == "left":
            first = "right"
            second = "left"
            self.height = source.height

            if direction == "right":
                self.pos[0] += source.width
        else:
            first = "up"
            second = "down"
            self.width = source.height

            if direction == "up":
                self.pos[1] += source.height

        self.ids.first.set_direction(first)
        self.ids.second.set_direction(second)

        if first == direction:
            self.ids.first.set_locations(source, destination)
            self.ids.second.set_locations(destination, source)
        else:
            self.ids.first.set_locations(destination, source)
            self.ids.second.set_locations(source, destination)


class ConnectionIcon(MDIconButton):
    is_active: bool
    direction: str
    source: 'Location'
    destination: 'Location'
    card: ObjectProperty(None)

    ACTIVE_COLOR = ColorProperty((1, 1, 1, 1))
    INACTIVE_COLOR = ColorProperty((0.6, 0.6, 0.6, 0.6))

    # we need right, left etc. naming for icons, but in JSON there are N, S, etc.
    direction_to_letter = {"right": "E", "left": "W", "up": "N", "down": "S"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_active = False

    def set_direction(self, direction: str):
        self.icon = f"chevron-{direction}"
        self.direction = ConnectionIcon.direction_to_letter[direction]

    def set_locations(self, source, destination):
        self.source = source
        self.destination = destination

    def on_press(self):
        if self.is_active:
            self.icon_color = self.INACTIVE_COLOR
            self.source.exits[self.direction] = None
        else:
            self.icon_color = self.ACTIVE_COLOR
            self.source.exits[self.direction] = self.destination

        self.is_active = not self.is_active
