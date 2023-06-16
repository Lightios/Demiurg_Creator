import json
import os
import shutil

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

from ui.dataclasses.quest import Quest
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
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.primary_hue = "50"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.theme_style = "Dark"

        prepare_assets()
        # Clock.schedule_once(lambda x: self.test())

    def test(self):
        self.root.ids.screen_manager.current = "creator"
        grid = self.root.ids.creator_screen.ids.grid
        button = grid.children[0]

        touch = MouseMotionEvent(None, 123, button.pos)  # args are device, id, spos
        touch.button = 'left'
        button.dispatch('on_touch_down', touch)

    def save_project(self):
        creator_screen = self.root.ids.creator_screen

        metadata = {
            "title": creator_screen.ids.project_name.text,
            "author": creator_screen.ids.project_author.text,
            "description": creator_screen.ids.project_description.text
        }

        grid = self.root.ids.creator_screen.ids.grid
        quests = self.root.ids.creator_screen.quests
        # path = filechooser.save_file(title="Select save location", filters=[(".json", "*.json")])

        dirname = os.path.dirname(__file__)
        demiurg_folder = os.path.dirname(dirname)
        projects_folder = os.path.join(demiurg_folder, "projects")
        new_project_folder = os.path.join(projects_folder, metadata["title"])
        toast_message = ""

        try:
            os.mkdir(new_project_folder)
        except FileExistsError:
            if metadata["title"] == "":
                toast("Project title cannot be empty")
                return
            else:
                toast_message += "Overwriting project. "

        path = os.path.join(new_project_folder, "data.json")
        self.runtime.save_project(metadata, grid, path, quests)
        toast_message += "Project saved!"
        toast(toast_message)

    def load_project(self, project: str | None = None):
        dirname = os.path.dirname(__file__)
        demiurg_folder = os.path.dirname(dirname)
        projects_folder = os.path.join(demiurg_folder, "projects")

        if project is None:
            path = filechooser.open_file(title="Select project to load", filters=[(".json", "*.json")])
            if not path:
                return
        else:
            project_folder = os.path.join(projects_folder, project)
            path = [os.path.join(project_folder, "data.json")]
        data = self.runtime.load_project(path[0])

        if project is None:
            title = data["metadata"]["title"]
            new_project_folder = os.path.join(projects_folder, title)
            try:
                os.mkdir(new_project_folder)
                json_object = json.dumps(data, indent=4)
                json.dumps("")

                with open(os.path.join(new_project_folder, "data.json"), "w") as outfile:
                    outfile.write(json_object)
            except FileExistsError:
                toast(f"Project {title} already exists")

        self.create_new_project()

        creator_screen = self.root.ids.creator_screen
        grid = self.root.ids.creator_screen.ids.grid
        grid.clear_widgets()

        creator_screen.ids.project_name.text = data["metadata"]["title"]
        creator_screen.ids.project_author.text = data["metadata"]["author"]
        creator_screen.ids.project_description.text = data["metadata"]["description"]

        # keys in JSON are always strings, we need ints here
        grid.row_counter = {int(k): int(v) for k, v in data["grid_parameters"]["row_counter"].items()}
        grid.column_counter = {int(k): int(v) for k, v in data["grid_parameters"]["column_counter"].items()}
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

            if parameters_location["is_start"]:
                grid.start_location = location

        for parameters_button in data["buttons"].values():
            button = ButtonLocation(
                row=parameters_button["row"],
                column=parameters_button["column"],
                pos=parameters_button["pos"],
                grid=grid
            )
            grid.locations[(button.row, button.column)] = button
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

        for quest_id, parameters_quest in data["quests"].items():
            quest = Quest()
            quest.name = parameters_quest["name"]
            quest.description = parameters_quest["description"]
            quest.starting_stage = parameters_quest["start_stage_id"]

            for stage_id, stage_parameters in parameters_quest["stages"].items():
                quest.stages[stage_id] = {
                    "text": stage_parameters["text"],
                    "options": stage_parameters["options"],
                    "location": location_ids[stage_parameters["location_id"]]
                }

            creator_screen.quests[quest_id] = quest

        self.root.ids.screen_manager.current = "creator"

    def export_game(self):
        grid = self.root.ids.creator_screen.ids.grid
        quests = self.root.ids.creator_screen.quests
        creator_screen = self.root.ids.creator_screen

        metadata = {
            "title": creator_screen.ids.project_name.text,
            "author": creator_screen.ids.project_author.text,
            "description": creator_screen.ids.project_description.text
        }

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
            self.runtime.export_game(metadata, locations,
                                     str(grid.start_location.location_id.int), path, quests)

    def delete_all(self):
        grid = self.root.ids.creator_screen.ids.grid
        grid.delete_all()

    def create_new_project(self):
        creator_screen = self.root.ids.creator_screen
        self.root.ids.screen_manager.remove_widget(creator_screen)

        creator_screen = CreatorScreen(name="creator")
        self.root.ids.screen_manager.add_widget(creator_screen)
        self.root.ids["creator_screen"] = creator_screen

        self.root.ids.screen_manager.current = "creator"

    def delete_project(self, project_title: str):
        dirname = os.path.dirname(__file__)
        demiurg_folder = os.path.dirname(dirname)
        projects_folder = os.path.join(demiurg_folder, "projects")
        project_folder = os.path.join(projects_folder, project_title)
        shutil.rmtree(project_folder)

        self.root.ids.menu_screen.reload_projects()


class NavigationButton(MDCard):
    text = StringProperty()
