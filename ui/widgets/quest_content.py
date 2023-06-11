
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.stacklayout import StackLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem

from ui.dataclasses.quest import Quest
from ui.widgets.oldschool_button import OldschoolButton
from ui.widgets.quest_stage import QuestStage

Builder.load_file('ui/widgets/quest_content.kv')


class QuestContent(StackLayout):
    current_quest: Quest

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_quest(self, quest: Quest):
        self.current_quest = quest
        self._recreate_menu()
        self._update_fields()
        self._recreate_stages()

    def _recreate_menu(self):
        menu_items = [
            {
                "viewclass": "IconListItem",
                "icon": "git",
                "text": f"{stage_id}",
                "height": dp(56),
                "on_release": lambda x=f"Item {i}": self.set_item(x),
            } for stage_id, stage in self.current_quest.stages
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.drop_item,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        self.menu.bind()

    def set_item(self, text_item):
        self.ids.drop_item.set_item(text_item)
        self.starting_stage =
        self.menu.dismiss()

    def add_new_stage(self):
        self.add_widget()

    def _update_fields(self):
        self.ids.name_field.text = self.current_quest.name
        self.ids.description_field.text = self.current_quest.description
        self.ids.starting_stage.text = f"Stage id: {self.current_quest.starting_stage}"

    def save_quest(self):
        self.current_quest.name = self.ids.name_field.text
        self.current_quest.description = self.ids.description_field.text
        self.current_quest.starting_stage = self.ids.starting_stage.text


class IconListItem(OneLineIconListItem):
    icon = StringProperty()
