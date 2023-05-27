from kivy.graphics import Color, Line
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from ui.widgets.location import Location
from ui.widgets.connection import Connection
from ui.widgets.button_location import ButtonLocation
from typing import List, Dict, Tuple

Builder.load_file('ui/widgets/grid.kv')

OFFSET = 10
LOCATION_SIZE = 200


class Grid(RelativeLayout):
    vertical_lines: List[Line]
    horizontal_lines: List[Line]
    locations: Dict[Tuple[int, int], Location | ButtonLocation]
    start_location: Location | None

    def __init__(self, **kw):
        super().__init__(**kw)

        self.init_lines()
        self.locations = dict()
        self.start_location = None

    def init_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            self.horizontal_lines = [Line(points=(0, 0, 0, self.height)) for _ in range(8)]
            self.vertical_lines = [Line(points=(0, 0, 0, self.height)) for _ in range(9)]

    def on_size(self, *args):
        self.update_lines()

    def update_lines(self):
        for i, line in enumerate(self.vertical_lines):
            width = LOCATION_SIZE * i + OFFSET
            line.points = (width, 0, width, self.height)

        for i, line in enumerate(self.horizontal_lines):
            height = self.height - (LOCATION_SIZE * i + OFFSET)
            line.points = (0, height, self.width, height)

    def add_location(self, button):
        location = Location(button)

        # center location on the button - Kivy renders widgets starting from bottom left corner
        # we need to subtract half of the sizes to render it properly
        location.pos = button.pos[0] - location.width // 2 + button.width // 2,\
            button.pos[1] - location.height // 2 + button.height // 2

        row, column = location.row, location.column

        self.locations[(row, column)] = location
        self.add_widget(location)

        # check all neighbours for created location
        for x, y, direction in ((1, 0, "right"), (-1, 0, "left"), (0, 1, "down"), (0, -1, "up")):
            new_row = row + y
            new_column = column + x

            # dont go outside the grid
            if new_row < 0 or new_column < 0:
                continue

            if not (new_row, new_column) in self.locations:
                new_button = ButtonLocation(row=new_row, column=new_column, pos=button.pos, grid=self)
                if row != new_row:
                    new_button.pos[1] = button.pos[1] - location.height * y  # move vertically
                else:
                    new_button.pos[0] = button.pos[0] + location.width * x  # move horizontally

                self.locations[(new_row, new_column)] = new_button
                self.add_widget(new_button)

            elif type(self.locations[(new_row, new_column)]) == Location:
                connection = Connection(direction=direction, source=location,
                                        destination=self.locations[(new_row, new_column)], pos=location.pos)

                self.add_widget(connection)

        self.remove_widget(button)
        del button
