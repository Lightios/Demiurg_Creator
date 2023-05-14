from kivy.graphics import *
from kivymd.uix.list import OneLineAvatarIconListItem


class ItemConfirm(OneLineAvatarIconListItem):
    # ta klasa pewnie będzie wywalona do innego pliku, ale na razie niech tu będzie
    divider = None

    def __init__(self, root, index: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = root
        self.index = index

    def set_icon(self, instance_check):
        # mark this and unmark others
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False

        # assign proper card for root
        if self.root.selecting_stage == 1:
            self.root.selected_one = self.root.cards[self.index]
        else:
            self.root.selected_two = self.root.cards[self.index]


class Connection(Line):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.temporary_points = [0, 0, 0, 0]  # temporary points are needed for moving connections; connections don't update if we change point list directly (don't know why)
        self.changed = False
