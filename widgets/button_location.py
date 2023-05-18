from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDIconButton

Builder.load_file('widgets/button_location.kv')


class ButtonLocation(MDIconButton):
    grid = ObjectProperty()



