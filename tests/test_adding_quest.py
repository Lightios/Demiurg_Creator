import unittest
from kivy.app import App
from kivy.lang import Builder
from kivy.tests.common import GraphicUnitTest, UnitTestTouch
from runtime.runtime import Runtime
from ui.ui import UI  # Import the app class from the separate Python file
import time
from unittest.mock import patch



class MyTestCase(GraphicUnitTest):

    def test_adding_location(self):
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

        #simulate clicking new project button
        new_pjct = ui.root.ids.new_project_btn
        new_pjct.dispatch('on_press')
        time.sleep(0.1)  # Pause for 0.1 seconds (adjust the delay if needed)
        self.assertEqual(ui.root.ids.nav_drawer.state, "close")
        self.assertEqual(ui.root.ids.screen_manager.current, "creator") #check if the creator screen has been launched

        #adding quest
        creator_screen = ui.root.ids.screen_manager.get_screen('creator')
        quest_btn = creator_screen.ids.quest_btn
        quest_btn.dispatch('on_press')
        with patch.object(creator_screen, 'open_quest_dialog') as mock_open_quest_dialog:
            quest_btn.dispatch('on_press')

            # Assert that the open_quest_dialog function was called once
            mock_open_quest_dialog.assert_called_once()
        

        ui.stop()# Clean up the app



        
   
        



