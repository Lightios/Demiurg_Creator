from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from plyer import filechooser
from kivymd.toast import toast

from ui.screens.menu_screen import MenuScreen
from ui.screens.creator_screen import CreatorScreen
from ui.assets_loader import prepare_assets
from ui.widgets.location import Location


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

    def save_project(self):
        project_title_label = self.root.ids.creator_screen.ids.project_title_label
        grid = self.root.ids.creator_screen.ids.grid

        locations = []
        for location in grid.locations.values():
            if isinstance(location, Location):
                locations.append(location)

        if grid.start_location is None:
            toast("You need to set a start location before saving")
            return

        path = filechooser.save_file(title="Select save location",
                                     filters=[(".json", "*.json")])
        
        # TODO: handle cancel

        path = path[0] if path[0].endswith(".json") else path[0] + ".json"  # filechooser returns a list, so we take [0]
        self.runtime.save_project(project_title_label.text, locations,
                                  str(grid.start_location.location_id.int), path)


class NavigationButton(MDCard):
    text = StringProperty()
