import unittest
from kivy.app import App
from kivy.lang import Builder
from kivy.tests.common import GraphicUnitTest, UnitTestTouch
from runtime.runtime import Runtime
from ui.ui import UI  # Import the UI class from the separate Python file


class MyTestCase(GraphicUnitTest):

    def test_button_press(self):
        # Create an instance of your UI class
        runtime = Runtime()
        ui = runtime.ui  # Pass the runtime object to the UI constructor
        menu_screen = ui.root.ids.screen_manager.get_screen('menu')
        menu_btn = menu_screen.ids.menu_button
        menu_btn.dispatch('on_press')  # Simulate a button press

        # Perform assertions on the expected behavior
        #self.assertEqual(ui.root.ids.nav_drawer.state, "open")

        # Clean up the UI
        ui.stop()


if __name__ == '_main_':
    unittest.main()