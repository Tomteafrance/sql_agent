from pydantic import BaseModel
from abc import ABC, abstractmethod

class BaseDBConnector(BaseModel, ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_database(self):
        pass