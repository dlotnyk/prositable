from typing import Tuple
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from defs.client_table_params import ClientTableParams
from defs.basic_defs import ClientType
client_table_suffix = "client_history_"


def create_client_table(table_name: str) -> Tuple:
    ClientBaseDef = declarative_base()

    class ClientTableDef(ClientBaseDef):
        """
        The main Table
        """
        __tablename__ = table_name
        entry_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
        date = db.Column(db.Date, nullable=False)
        client_type = db.Column(db.Enum(ClientType), nullable=False)
        tasks = db.Column(db.Unicode)
        notes = db.Column(db.Unicode)

        def __init__(self, **kwargs):
            try:
                params = ClientTableParams(kwargs)
                self.entry_id = params.entry_id
                self.date = params.date
                self.client_type = params.client_type
                self.tasks = params.tasks
                self.notes = params.notes
            except KeyError:
                pass

        @classmethod
        def set_table_name(cls, value: str):
            cls.__tablename__ = value

        def __repr__(self):
            return f"Client_table_{self.client_id}"

    return ClientTableDef, ClientBaseDef
