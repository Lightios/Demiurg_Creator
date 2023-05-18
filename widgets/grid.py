from kivy.graphics import Color, Line
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from widgets.location import Location
from widgets.button_location import ButtonLocation

Builder.load_file('widgets/grid.kv')


class Grid(RelativeLayout):
    vertical_lines = []
    horizontal_lines = []

    def __init__(self, **kw):
        super().__init__(**kw)

        self.init_lines()

    def on_size(self, *args):
        self.update_lines()

    def init_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            self.horizontal_lines = [Line(points=(0, 0, 0, self.height)) for _ in range(8)]
            self.vertical_lines = [Line(points=(0, 0, 0, self.height)) for _ in range(8)]

    def update_lines(self):
        for i, line in enumerate(self.vertical_lines):
            width = 200 * i + 10  # offset
            line.points = (width, 0, width, self.height)

        for i, line in enumerate(self.horizontal_lines):
            height = self.height - (200 * i + 10)  # offset
            line.points = (0, height, self.width, height)

    def add_location(self, button):
        location = Location(pos=button.pos)
        location.pos = button.pos[0] - location.width // 2 + button.width // 2,\
            button.pos[1] - location.height // 2 + button.height // 2  # looks complicated but it centers the location

        self.add_widget(location)

        button_right = ButtonLocation(pos=button.pos, grid=self)
        button_right.pos[0] = button.pos[0] + location.width

        button_down = ButtonLocation(pos=button.pos, grid=self)
        button_down.pos[1] = button.pos[1] - location.height

        self.add_widget(button_right)
        self.add_widget(button_down)
