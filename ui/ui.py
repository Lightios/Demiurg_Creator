from kivy.clock import Clock
from kivy.input.providers.mouse import MouseMotionEvent
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from plyer import filechooser
from kivymd.toast import toast
import gc

from ui.screens.menu_screen import MenuScreen
from ui.screens.creator_screen import CreatorScreen
from ui.assets_loader import prepare_assets
from ui.widgets.button_location import ButtonLocation
from ui.widgets.location import Location
from ui.widgets.grid import Grid
from ui.widgets.connection import Connection


class ContentNavigationDrawer(RelativeLayout):
    pass


class UI(MDApp):
    def __init__(self, runtime, **kwargs):
        super().__init__(**kwargs)
        self.runtime = runtime

    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.theme_style = "Dark"

        prepare_assets()
        Clock.schedule_once(lambda x: self.test())

    def test(self):
        self.root.ids.screen_manager.current = "creator"
        grid = self.root.ids.creator_screen.ids.grid
        button = grid.children[0]

        touch = MouseMotionEvent(None, 123, button.pos)  # args are device, id, spos
        touch.button = 'left'
        button.dispatch('on_touch_down', touch)

    def save_project(self):
        metadata = {
            "title": "a",
            "author": "b",
            "description": "c"
        }

        grid = self.root.ids.creator_screen.ids.grid
        path = filechooser.save_file(title="Select save location", filters=[(".json", "*.json")])

        if path:
            path = path[0] if path[0].endswith(".json") else path[
                                                                 0] + ".json"  # filechooser returns a list, so we take [0]
            self.runtime.save_project(metadata, grid, path)

    def load_project(self):
        grid = self.root.ids.creator_screen.ids.grid
        grid.delete_all()

        path = filechooser.open_file(title="Select project to load", filters=[(".json", "*.json")])
        data = self.runtime.load_project(path[0])

        grid.row_counter = data["grid_parameters"]["row_counter"]
        grid.column_counter = data["grid_parameters"]["column_counter"]
        grid.max_row_quantity = data["grid_parameters"]["max_row_quantity"]
        grid.max_column_quantity = data["grid_parameters"]["max_column_quantity"]
        grid.size = data["grid_parameters"]["size"]

        location_ids = dict()
        for parameters_location in data["locations"].values():
            location = Location(
                row=parameters_location["row"],
                column=parameters_location["column"]
            )
            location.update_parameters(parameters_location)
            grid.add_widget(location)
            grid.locations[(location.row, location.column)] = location
            location_ids[parameters_location["location_id"]] = location

        # for parameters_location in data["locations"].values():
        #     location = location_ids[parameters_location["location_id"]]
        #
        #     for key, destination in parameters_location["exits"].items():
        #         location[key] = location_ids[destination]

        for parameters_button in data["buttons"].values():
            button = ButtonLocation(
                row=parameters_button["row"],
                column=parameters_button["column"],
                pos=parameters_button["pos"],
                grid=grid
            )
            grid.add_widget(button)

        for parameters_connection in data["connections"].values():
            source = location_ids[parameters_connection["source"]]
            destination = location_ids[parameters_connection["destination"]]

            connection = Connection(
                direction=parameters_connection["direction"],
                source=source,
                destination=destination,
                pos=source.pos,  # connection's init repositions it basing on the source
            )

            if parameters_connection["first_is_active"]:
                connection.ids.first.on_press()

            if parameters_connection["second_is_active"]:
                connection.ids.second.on_press()

            grid.connections[((source.row, source.column), (destination.row, destination.column))] = connection
            grid.add_widget(connection)

    def export_game(self):
        project_title_label = self.root.ids.creator_screen.ids.project_title_label
        grid = self.root.ids.creator_screen.ids.grid

        locations = []
        for location in grid.locations.values():
            if isinstance(location, Location):
                locations.append(location)

        if grid.start_location is None:
            toast("You need to set a start location before saving")
            return

        path = filechooser.save_file(title="Select save location", filters=[(".json", "*.json")])

        if path:
            path = path[0] if path[0].endswith(".json") else path[0] + ".json"  # filechooser returns a list, so we take [0]
            self.runtime.export_game(project_title_label.text, locations,
                                     str(grid.start_location.location_id.int), path)

    def delete_all(self):
        grid = self.root.ids.creator_screen.ids.grid
        grid.delete_all()


class NavigationButton(MDCard):
    text = StringProperty()
