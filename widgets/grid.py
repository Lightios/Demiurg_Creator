from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from widgets.location import Location
from widgets.card_button import CardButton

Builder.load_file('widgets/grid.kv')


class Grid(RelativeLayout):
    def add_location(self, button):

        location = Location( pos=button.pos )
        location.pos = button.pos[0] - location.width // 2, button.pos[1] - location.height // 2

        self.add_widget( location )

        button_right = CardButton( pos=button.pos, grid=self )
        button_right.pos[0] = button.pos[0] + location.width

        button_down = CardButton( pos=button.pos, grid=self )
        button_down.pos[1] = button.pos[1] - location.height

        self.add_widget( button_right )
        self.add_widget( button_down )
