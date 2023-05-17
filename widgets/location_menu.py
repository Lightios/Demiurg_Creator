from kivy.uix.relativelayout import RelativeLayout


class LocationMenu( RelativeLayout ):
    def set_state(self, state: str):
        if state == "open":
            self.pos_hint = {"x": 0.1}

        else:
            self.pos_hint = {"x": -0.5}  # hide
