from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from langchain_community.utilities import SQLDatabase
from base import BaseDBConnector

class LocalDBConnector(BaseDBConnector):
    username: str
    password: str
    database_name: str
    host: str
    port: str
    table_list: str

    def get_database_path(self) -> str:
        return f"postegresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.database_name}"

    def connect(self) -> Engine:
        return create_engine(f"sqlite://{self.get_database_path()}")
    
    def get_database(self) -> SQLDatabase:
        return SQLDatabase.from_uri(self.get_database_path(), sample_rows_in_table_info=1, include_tables=self.table_list, view_support=True, schema="public")
    