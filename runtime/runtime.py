from dataclasses import dataclass
from typing import Dict, List
import json

from runtime.i_runtime import IRuntime
from ui.ui import UI
from ui.widgets.location import Location


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

    def export_game(self,
                    metadata: dict,
                    locations: Dict,
                    start_location_id: str,
                    path: str,
                    quests: Dict[int, 'Quest'],
                    ):
        dictionary = {
            "metadata": metadata,

            "map": {
                "start_location_id": start_location_id,
                "locations": {}
            },

            "quests": {

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
                    description = location.exit_descriptions[exit]
                    if description == "":
                        description = "Go " + exit

                    loc_dict["exits"][exit] = {
                        "location_id": f"{destination.location_id.int}",
                        "text": description
                    }

            dictionary["map"]["locations"][location.location_id.int] = loc_dict

        for quest_id, quest in quests.items():
            quest_dict = {
                "name": quest.name,
                "description": quest.description,
                "start_stage_id": quest.starting_stage,
                "stages": {}
            }

            for stage_id, stage in quest.stages.items():
                quest_dict["stages"][stage_id] = {
                    "location_id": str(stage["location"].location_id.int),
                    "text": stage["text"],
                    "options": {}
                }

                for option_id, option in stage["options"].items():
                    quest_dict["stages"][stage_id]["options"][option_id] = {
                        "text": option["text"],
                        "next_stage_id": option["next_stage_id"],
                        "response_message": option["response_message"],
                    }

            dictionary["quests"][quest_id] = quest_dict

        json_object = json.dumps(dictionary, indent=4)
        json.dumps("")

        with open(path, "w") as outfile:
            outfile.write(json_object)

    def save_project(self, metadata: dict, grid, path: str, quests: dict):
        dictionary = {
            "metadata": {
                "title": metadata["title"],
                "author": metadata["author"],
                "description": metadata["description"],
            },

            "grid_parameters": {
                "row_counter": grid.row_counter,
                "column_counter": grid.column_counter,
                "max_row_quantity": grid.max_row_quantity,
                "max_column_quantity": grid.max_column_quantity,
                "size": grid.size,
            },

            "locations": {},
            "buttons": {},
            "connections": {},
            "quests": {},
        }

        i = 0
        for item in grid.locations.values():
            if type(item) == Location:
                loc_dict = {
                    "name": item.name,
                    "description": item.description,
                    "is_start": item.is_start,
                    "is_end": item.is_end,

                    "pos": item.pos,
                    "location_id": item.location_id.int,
                    "row": item.row,
                    "column": item.column,
                    "exits": {},
                    "exit_descriptions": {
                        "N": item.exit_descriptions["N"],
                        "E": item.exit_descriptions["E"],
                        "S": item.exit_descriptions["S"],
                        "W": item.exit_descriptions["W"],
                    }
                }

                for key, destination in item.exits.items():
                    if destination is not None:
                        loc_dict["exits"][key] = destination.location_id.int

                dictionary["locations"][item.location_id.int] = loc_dict
            else:
                i += 1
                button_dict = {
                    "pos": item.pos,
                    "row": item.row,
                    "column": item.column,
                }

                dictionary["buttons"][i] = button_dict

        for connection in grid.connections.values():
            conn_dict = {
                "direction": connection.direction,
                "source": connection.source.location_id.int,
                "destination": connection.destination.location_id.int,
                "first_is_active": connection.ids.first.is_active,
                "second_is_active": connection.ids.second.is_active,
            }

            dictionary["connections"][i] = conn_dict
            i += 1

        for quest_id, quest in quests.items():
            quest_dict = {
                "name": quest.name,
                "description": quest.description,
                "start_stage_id": quest.starting_stage,
                "stages": {}
            }

            for stage_id, stage in quest.stages.items():
                quest_dict["stages"][stage_id] = {
                    "location_id": stage["location"].location_id.int,
                    "text": stage["text"],
                    "options": {}
                }

                for option_id, option in stage["options"].items():
                    quest_dict["stages"][stage_id]["options"][option_id] = {
                        "text": option["text"],
                        "next_stage_id": option["next_stage_id"],
                        "response_message": option["response_message"],
                    }

            dictionary["quests"][quest_id] = quest_dict

        json_object = json.dumps(dictionary, indent=4)
        json.dumps("")

        with open(path, "w") as outfile:
            outfile.write(json_object)

    def load_project(self, path: str) -> dict:
        file = open(path)
        data = json.load(file)
        file.close()
        return data
