from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog

Builder.load_file('ui/widgets/project_card.kv')


class ProjectCard(MDCard):
    project_title = StringProperty("Project Title")

    def __init__(self, project_title, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project_title = project_title
        self.dialog = None

    def show_delete_dialog(self):
        def delete():
            App.get_running_app().delete_project(self.project_title)
            self.dialog.dismiss()

        self.dialog = MDDialog(
            title="Delete project?",
            text="Warning: You cannot undo this action",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_press=lambda x: self.dialog.dismiss(),
                ),
                MDFlatButton(
                    text="DELETE",
                    on_press=lambda x: delete(),
                ),
            ],
        )
        self.dialog.open()
