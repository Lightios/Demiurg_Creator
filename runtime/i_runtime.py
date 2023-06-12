import uuid
from abc import ABC, abstractmethod
from typing import Dict


class IRuntime(ABC):
    """
    Interface for the runtime. This is the interface that the UI uses to
    communicate with the runtime.
    """

    @abstractmethod
    def export_game(self, title: str, locations, start_location_id, path, quests) -> None:
        pass

    @abstractmethod
    def save_project(self, metadata: dict, grid, path: str, quests) -> None:
        pass

    @abstractmethod
    def load_project(self, path: str) -> dict:
        pass




