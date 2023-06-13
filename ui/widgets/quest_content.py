
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.stacklayout import StackLayout
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem

from ui.dataclasses.quest import Quest
from ui.widgets.oldschool_button import OldschoolButton
from ui.widgets.quest_stage import QuestStage

Builder.load_file('ui/widgets/quest_content.kv')


class QuestContent(StackLayout):
    current_quest: Quest | None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stages = dict()
        self.starting_stage = None
        self.current_quest = None

    def set_quest(self, quest: Quest):
        self.current_quest = quest
        self._recreate_menu()
        self._update_fields()
        self._recreate_stages()

    def _recreate_menu(self):
        menu_items = [
            {
                "viewclass": "OneLineIconListItem",
                "icon": "git",
                "text": f"{stage_id}",
                "height": dp(56),
                "on_release": lambda x=stage_id, y=stage: self.set_item(x, y),
            } for stage_id, stage in self.current_quest.stages.items()
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.starting_stage,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        self.menu.bind()

    def _update_fields(self):
        self.ids.name_field.text = self.current_quest.name
        self.ids.description_field.text = self.current_quest.description
        self.ids.starting_stage.set_item(f"{self.current_quest.starting_stage}")

    def _recreate_stages(self):
        for stage in self.stages.values():
            self.remove_widget(stage)

        self.stages = dict()

        for stage_id, stage in self.current_quest.stages.items():
            self.add_new_stage(stage_id, stage)

    def set_item(self, stage_id, stage):
        self.ids.starting_stage.set_item(f"{stage_id}")
        self.starting_stage = stage
        self.menu.dismiss()

    def add_new_stage(self, stage_id: int | None = None, stage=None):
        button = self.ids.add_new_stage_button

        if stage_id is None:
            # if stage_id is None, we are creating new stage using a button
            # otherwise it's loaded from already existing stage
            stage_id = self.current_quest.generate_id_for_stage()
            self.current_quest.add_new_stage(stage_id)
            self._recreate_menu()

        stage = QuestStage(stage_id, stage, self.current_quest)
        self.stages[stage_id] = stage
        self.add_widget(stage)

        # make the button be at bottom of this layout
        self.remove_widget(button)
        self.add_widget(button)

    def save_quest(self) -> bool:
        """
        Tries to save current quest, if fails, returns False
        """
        if self.current_quest is None:
            return False

        for stage in self.stages.values():
            if stage.location is None:
                toast("Location not set")
                return False

            for option in stage.options.values():
                if option.ids.stage_select.current_item is None:
                    toast("Stage not set")
                    return False

        self.current_quest.name = self.ids.name_field.text
        self.current_quest.description = self.ids.description_field.text
        self.current_quest.starting_stage = self.ids.starting_stage.current_item

        for stage_id, stage in self.stages.items():
            temp_dict = {
                "location": stage.location,
                "text": stage.ids.text_field.text,
                "options": {}
            }

            for option_id, option in stage.options.items():
                temp_dict["options"][option_id] = {
                    "text": option.ids.text_field.text,
                    "next_stage_id": option.ids.stage_select.current_item,
                    "response_message": option.ids.message_field.text,
                }

            self.current_quest.stages[stage_id] = temp_dict

        return True
