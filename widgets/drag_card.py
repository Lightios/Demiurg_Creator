from kivy.lang import Builder
from kivy.uix.behaviors import DragBehavior
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, ObjectProperty


Builder.load_file('widgets/drag_card.kv')


class DragCard(DragBehavior, MDCard):
    # min and max x for cards - they can't be moved outside their layout; set in Creator Screen
    MIN_X = 0
    MAX_X = 0

    creator_screen = ObjectProperty()
    text = StringProperty("New Location")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.attached_connections_in = []
        self.attached_connections_out = []

    def on_touch_move(self, touch):
        super(DragCard, self).on_touch_move(touch)

        # prevent moving outside layout
        self.x = min(self.x, self.MAX_X)
        self.x = max(self.x, self.MIN_X)

        # update connections
        for connection in self.attached_connections_out:
            connection.temporary_points[0] = self.x + self.width / 2
            connection.temporary_points[1] = self.y + self.height / 2
            connection.changed = True

        for connection in self.attached_connections_in:
            connection.temporary_points[2] = self.x + self.width / 2
            connection.temporary_points[3] = self.y + self.height / 2
            connection.changed = True

        self.creator_screen.update_lines()
