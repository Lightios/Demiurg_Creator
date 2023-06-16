import unittest
from kivy.app import App
from kivy.lang import Builder
from kivy.tests.common import GraphicUnitTest, UnitTestTouch
from runtime.runtime import Runtime
from ui.ui import UI  # Import the app class from the separate Python file
import time
from unittest.mock import patch



class MyTestCase(GraphicUnitTest):

    def test_load_project(self):
        runtime = Runtime()
        ui =  UI(runtime)
        ui.build()
        with open("ui/ui.kv", 'r') as file:
            root_content = file.read()
        ui.root = Builder.load_string(root_content)

       
        #simulate opening of the side menu
        menu_screen = ui.root.ids.screen_manager.get_screen('menu')
        menu_btn = menu_screen.ids.menu_button
        menu_btn.dispatch('on_press')  # Simulate a button press
        self.assertEqual(ui.root.ids.nav_drawer.state, "open")

        #simulate clicking load button
        load_btn = ui.root.ids.load_btn
        load_btn.dispatch('on_press')
        with patch.object(ui, 'load_project') as mock_load_project:
            ui.load_project()

            # Assert that the load_project function was called once
            mock_load_project.assert_called_once()
        


        ui.stop()# Clean up the app



        
   
        



