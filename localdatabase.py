from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from langchain_community.utilities import SQLDatabase
from base import BaseDBConnector

class LocalDBConnector(BaseDBConnector):
    database_path: str

    def connect(self) -> Engine:
        return create_engine(f"sqlite://{self.database_path}")
    
    def get_database(self) -> SQLDatabase:
        return SQLDatabase.from_uri(f"sqlite:///{self.database_path}")
    