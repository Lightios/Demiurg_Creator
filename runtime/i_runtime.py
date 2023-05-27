import uuid
from abc import ABC, abstractmethod
from typing import Dict

# Data to be written


# Serializing json


# from models.game_data import Exit, Location


class IRuntime(ABC):
    """
    Interface for the runtime. This is the interface that the UI uses to
    communicate with the runtime.
    """

    @abstractmethod
    def save_project(self, title: str, locations, start_location_id, path) -> None:
        pass






