from kivy.graphics import Color, Line
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivymd.toast import toast

from ui.widgets.location import Location
from ui.widgets.connection import Connection, ConnectionIcon
from ui.widgets.button_location import ButtonLocation
from typing import List, Dict, Tuple

Builder.load_file('ui/widgets/grid.kv')

OFFSET = 10
LOCATION_SIZE = 200


def get_opposite_direction(direction: str):
    return {"E": "W", "N": "S", "W": "E", "S": "N"}[direction]


class Grid(RelativeLayout):
    vertical_lines: List[Line]
    horizontal_lines: List[Line]
    locations: Dict[Tuple[int, int], Location | ButtonLocation]

    # like edges in graph, first tuple is row and column of one location
    # second tuple is row and column of second location
    connections: Dict[Tuple[Tuple[int, int], Tuple[int, int]], Connection]

    start_location: Location | None

    def __init__(self, **kw):
        super().__init__(**kw)

        self.init_lines()
        self.locations = dict()
        self.start_location = None
        self.connections = dict()

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

            # don't go outside the grid
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
                item = self.locations[(new_row, new_column)]
                connection = Connection(direction=direction, source=location,
                                        destination=item, pos=location.pos)

                self.connections[((location.row, location.column), (item.row, item.column))] = connection
                self.add_widget(connection)

        self.remove_widget(button)
        del button

    def delete_location(self, location: Location):
        if not self.check_graph_connection(location):
            toast("Can't remove this location")
            return

        # replace the location with a button
        button = ButtonLocation(row=location.row, column=location.column, grid=self, pos=location.pos)
        button.pos = button.pos[0] + location.width // 2 - button.width // 2,\
            button.pos[1] + location.height // 2 - button.height // 2  # recenter
        self.locations[(location.row, location.column)] = button
        self.add_widget(button)

        # check neighbours
        for x, y, direction in ((1, 0, "E"), (-1, 0, "W"), (0, 1, "S"), (0, -1, "N")):
            new_row = location.row + y
            new_column = location.column + x

            if (new_row, new_column) in self.locations:
                item = self.locations[(new_row, new_column)]

                if type(item) == ButtonLocation:
                    # if there's nearby button location, check if this button has any other nearby location
                    # if not, delete it
                    found_location = False
                    for temp_x, temp_y in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        temp_row = new_row + temp_y
                        temp_column = new_column + temp_x

                        if (temp_row, temp_column) in self.locations:
                            if type(self.locations[(temp_row, temp_column)]) == Location:
                                found_location = True

                    if not found_location:
                        self.remove_widget(item)
                        self.locations.pop((new_row, new_column))

                elif type(item) == Location:
                    opposite_direction = get_opposite_direction(direction)
                    item.exits[opposite_direction] = None
                    item.exit_descriptions[opposite_direction] = ""

                    # remove connection
                    tuple_key = ((location.row, location.column), (new_row, new_column))
                    if tuple_key not in self.connections:
                        tuple_key = ((new_row, new_column), (location.row, location.column))

                    connection = self.connections[tuple_key]
                    self.connections.pop(tuple_key)
                    self.remove_widget(connection)

        if location.is_start:
            self.start_location = None

        self.remove_widget(location)

    def check_graph_connection(self, location: Location) -> bool:
        """
        BFS to check if graph would have connection without location given in parameter
        If it would, allow to delete it
        """

        # get locations only (skip buttons)
        locations = [loc for loc in self.locations.values() if type(loc) == Location]
        current = locations[0]

        if current == location:
            if len(locations) > 1:
                current = locations[1]
            else:
                return True

        to_visit = [current]
        visited = set()

        while len(to_visit) > 0:
            current = to_visit.pop(0)
            visited.add(current)

            for x, y in ((-1, 0), (1, 0), (0, 1), (0, -1)):
                row = current.row + y
                column = current.column + x

                if (row, column) in self.locations:
                    item = self.locations[(row, column)]
                    if item is not location and type(item) == Location and item not in visited:
                        to_visit.append(item)

        return len(visited) == len(locations) - 1
