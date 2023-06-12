from uuid import uuid4

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu

Builder.load_file('ui/widgets/quest_stage.kv')


class QuestStage(MDCard):
    location_name = StringProperty()
    text = StringProperty()
    id_text = StringProperty()
    stage_id: int
    options: dict

    def __init__(self, stage_id, stage, quest, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stage_id = stage_id
        self.current_quest = quest
        self.location = None
        self._recreate_menu()

        self.id_text = f"Stage id: {self.stage_id}"
        self.options = {}

        if stage is not None:
            self.location_id = stage["location_id"]
            self.text = stage["text"]
        else:
            self.text = "New description"

    def add_new_option(self):
        button = self.ids.add_new_option_button

        self.ids.stack.remove_widget(button)

        option = StageOption(self)
        self.options[option.id] = option

        self.ids.stack.add_widget(option)
        self.ids.stack.add_widget(button)

        self.height += option.height + self.ids.stack.spacing[1]  # offset

    def _recreate_menu(self):
        grid = App.get_running_app().root.ids.creator_screen.ids.grid
        locations = []
        for item in grid.locations.values():
            if isinstance(item, MDCard):
                locations.append(item)

        menu_items = [
            {
                "viewclass": "OneLineIconListItem",
                "icon": "git",
                "text": f"{location.name}",
                "height": dp(56),
                "on_release": lambda x=location: self.set_item(x),
            } for location in locations
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.location_select,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        self.menu.bind()

    def set_item(self, location):
        self.ids.location_select.set_item(f"{location.name}")
        self.location = location
        self.menu.dismiss()


class StageOption(MDCard):
    def __init__(self, stage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stage = stage
        self._recreate_menu()
        self.option_id = uuid4().int

    def remove(self):
        self.stage.remove(self)

    def _recreate_menu(self):
        menu_items = [
            {
                "viewclass": "OneLineIconListItem",
                "icon": "git",
                "text": f"{stage_id}",
                "height": dp(56),
                "on_release": lambda x=stage_id: self.set_item(x),
            } for stage_id in self.stage.current_quest.stages.keys()
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.stage_select,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        self.menu.bind()

    def set_item(self, stage_id):
        self.ids.stage_select.set_item(f"{stage_id}")
        self.menu.dismiss()
