import json
import pandas as pd
from sqlalchemy import MetaData
from sqlalchemy.engine.base import Engine

class DataLoader:
    def load_data(file) -> pd.DataFrame:
        if file.type == 'text/csv':
            dataframe = pd.read_csv(file)
        elif file.type == 'application/octet-stream':
            dataframe = pd.read_parquet(file)
        elif file.type == 'orc':
            dataframe = pd.read_orc(file)
        else:
            print('Unsupported file type')
        for col in dataframe:
            if dataframe[col].apply(lambda x: isinstance(x, dict)).any():
                dataframe[col] = dataframe[col].apply(lambda x: str(x) if isinstance(x, dict) else x)
        return dataframe

    def load_config(file) -> dict:
        return json.load(file)
            
    def drop_data(engine: Engine):
        meta = MetaData()
        meta.reflect(bind=engine)
        meta.drop_all(bind=engine)
        