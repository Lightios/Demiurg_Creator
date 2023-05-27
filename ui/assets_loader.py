from kivy.config import Config
from kivy.core.window import Window
from kivy.core.text import LabelBase


def prepare_assets():
    LabelBase.register(name='Monoton', fn_regular='ui/assets/Monoton-Regular.ttf')
    LabelBase.register(name='Nunito', fn_regular='ui/assets/Nunito-VariableFont_wght.ttf')
    LabelBase.register(name='Nunito_bold', fn_regular='ui/assets/Nunito-Bold.ttf')

    Window.size = (1400, 800)
    Window.top = 10
    Window.left = 10

    Config.set('input', 'mouse', 'mouse,disable_multitouch')

