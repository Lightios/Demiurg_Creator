from dataclasses import dataclass
from typing import List, Dict
# from ui.widgets.quest_stage import QuestStage
from uuid import uuid4, UUID


@dataclass
class Quest:
    name: str
    description: str
    starting_stage: int | None
    stages: Dict[int, Dict[str, str | int | Dict[str, str | int]]]
    id: int

    def __init__(self):
        self.name = "New quest"
        self.description = "New description"
        self.stages = {}
        self.starting_stage = None
        self.id = uuid4().int

    def generate_id_for_stage(self):
        if len(self.stages.keys()) == 0:
            return 1

        i = max(self.stages.keys())
        return i + 1

    def add_new_stage(self, stage_id: int):
        self.stages[stage_id] = {
            "location_id": "",
            "text": "",
            "options": {
                "text": "",
                "next_stage_id": "",
                "response_message": ""
            }
        }
