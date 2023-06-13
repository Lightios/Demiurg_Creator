from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.card import MDCard


Builder.load_file('ui/widgets/project_card.kv')


class ProjectCard(MDCard):
    project_title = StringProperty("Project Title")

    def __init__(self, project_title, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project_title = project_title
