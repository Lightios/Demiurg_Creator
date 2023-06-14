from typing import Dict

from kivy.graphics import Color
from kivy.lang import Builder
from kivymd.toast import toast
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from ui.dataclasses.quest import Quest
from ui.widgets.button_location import ButtonLocation
from ui.widgets.grid import Grid
from ui.widgets.location import Location
from ui.widgets.quest_content import QuestContent


Builder.load_file('ui/screens/creator_screen.kv')


class CreatorScreen(MDScreen):
    quests: Dict[int, Quest]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quests = {}
        self.dialog = None
        self.selected_item = None
        self.current_content = "grid"

    def update_name(self, textfield):
        self.ids.project_title_label.text = textfield.text

    def show_project(self):
        self.ids.project_content.pos_hint = {"x": 0.15, "y": 0.2}
        self.ids.scroll_grid.pos_hint = {"x": -10, "y": -10}
        self.ids.scroll_quests.pos_hint = {"x": -10, "y": -10}
        self.current_content = "project"

    def show_grid(self):
        # if self.current_content != "quest" or self.ids.quest_content.save_quest():  # if could save
        self.ids.project_content.pos_hint = {"x": -10, "y": -10}
        self.ids.scroll_grid.pos_hint = {"x": 0.1, "y": 0}
        self.ids.scroll_quests.pos_hint = {"x": -10, "y": -10}
        self.current_content = "grid"

    def open_quest_dialog(self):
        items = [ItemConfirm(self, text="Create a new quest")]

        for quest in self.quests.values():
            items.append(ItemConfirm(self, quest=quest, text=f"{quest.name}"))

        self.dialog = MDDialog(
            title="Select quest to edit",
            type="confirmation",
            items=items,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    on_press=lambda x: self.dialog.dismiss(),
                ),
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    on_press=lambda x: self.show_quest_content(),
                ),
            ],
        )

        self.dialog.open()

    def show_quest_content(self):
        if self.selected_item is None:
            toast("You need to select one item from list")
            return

        if self.selected_item.quest is None:
            quest_copy = Quest()
        else:
            quest_copy = Quest(self.selected_item.quest)

        self.ids.quest_content.set_quest(quest_copy)
        self.dialog.dismiss()

        self.ids.project_content.pos_hint = {"x": -10, "y": -10}
        self.ids.scroll_grid.pos_hint = {"x": -10, "y": -10}
        self.ids.scroll_quests.pos_hint = {"x": 0.2, "y": -0.02}
        self.current_content = "quest"
        self.selected_item = None

    def delete_all(self):
        del self.quests
        self.quests = dict()
        self.selected_item = None

    def save_quest(self, quest):
        self.quests[quest.id] = quest


class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def __init__(self, creator_screen, quest=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.creator_screen = creator_screen
        self.quest = quest

    def set_icon(self, instance_check):
        self.creator_screen.selected_item = self

        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False
