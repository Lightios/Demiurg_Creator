import os

from kivy.graphics import Color
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
# from widgets.connection import ItemConfirm, Connection
# from widgets.drag_card import DragCard
from ui.widgets.project_card import ProjectCard
from kivy.app import App

Builder.load_file('ui/screens/menu_screen.kv')


class MenuScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.app = App.get_running_app()
        self.loaded = False

    def on_kv_post(self, *args):
        self.add_project_cards()
        self.loaded = True

    def on_enter(self, *args):
        if self.loaded:
            self.reload_projects()

    def get_available_projects(self):
        dirname = os.path.dirname(__file__)
        ui = os.path.dirname(dirname)
        demiurg_folder = os.path.dirname(ui)
        projects_folder = os.path.join(demiurg_folder, "projects")

        folders = [x[0] for x in os.walk(projects_folder)]
        projects = []

        for folder in folders:
            project = folder.replace(projects_folder, "")
            project = project.replace("\\", "")
            project = project.replace("/", "")

            if project != "":
                projects.append(project)

        return projects

    def add_project_cards(self):
        projects = self.get_available_projects()

        for project in projects:
            card = ProjectCard(project_title=project)
            self.ids.stack.add_widget(card)

    def reload_projects(self):
        to_remove = self.ids.stack.children[:]
        for child in to_remove:
            self.ids.stack.remove_widget(child)

        self.add_project_cards()

