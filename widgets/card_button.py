from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDIconButton

Builder.load_file('widgets/card_button.kv')


class CardButton(MDIconButton):
    grid = ObjectProperty()



