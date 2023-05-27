from dataclasses import dataclass
from typing import Dict
import json

from runtime.i_runtime import IRuntime
from ui.ui import UI



@dataclass
class Runtime(IRuntime):
    """
    Runtime acts as a bridge between the UI and the game data. It is responsible for
    keeping track of the game progress and updating the UI when necessary.

    It also exposes some methods via the IRuntime interface that the UI can use to get
    information about the game progress (e.g. get_current_location) and
    to handle user actions (e.g. select_exit).
    """

    def __init__(self):
        self.ui = UI(self)
        self.ui.run()

    def save_project(self, title: str, locations: Dict, start_location_id: str, path: str):
        dictionary = {
            "metadata": {
                "title": title,
                "author": "Eldorado Games",
                "description": "Very short game about a very brave Roomba."
            },

            "map": {
                "start_location_id": start_location_id,
                "locations": {}
            }

        }

        for location in locations:
            loc_dict = {
                "name": location.name,
                "text": location.description,
                "exits": {}
            }

            if location.is_end:
                loc_dict["is_end_location"] = True

            for exit, destination in location.exits.items():
                if destination is not None:
                    loc_dict["exits"][exit] = {
                        "location_id": f"{destination.location_id.int}",
                        "text": "Go " + exit
                    }

            dictionary["map"]["locations"][location.location_id.int] = loc_dict

        json_object = json.dumps(dictionary, indent=4)
        json.dumps("")

        # Writing to sample.json
        with open(path, "w") as outfile:
            outfile.write(json_object)
