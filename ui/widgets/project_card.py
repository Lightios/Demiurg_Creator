from kivy.lang import Builder
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.card import MDCard


Builder.load_file('ui/widgets/project_card.kv')


class ProjectCard(MDCard):
    # def on_enter(self, *args):
    #     """The method will be called when the mouse cursor
    #     is within the borders of the current widget."""
    #
    #     self.md_bg_color = (1, 1, 1, 1)
    #
    # def on_leave(self, *args):
    #     """The method will be called when the mouse cursor goes beyond
    #     the borders of the current widget."""
    #
    #     self.md_bg_color = self.theme_cls.bg_darkest
    pass