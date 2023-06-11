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
    id: UUID

    def __init__(self):
        self.name = "New quest"
        self.description = "New description"
        self.stages = {}
        self.starting_stage = None
        self.id = uuid4()


