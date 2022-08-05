import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from coop_table_params import CoopTableParams
from basic_defs import CoopType
coop_table_suffix = "coop_history_"


def create_coop_table(table_name: str):
    CoopBaseDef = declarative_base()

    class CoopTableDef(CoopBaseDef):
        """
        The main Table
        """
        __tablename__ = table_name
        entry_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
        date = db.Column(db.Date, nullable=False)
        coop_type = db.Column(db.Enum(CoopType), nullable=True)
        tasks = db.Column(db.Unicode)
        notes = db.Column(db.Unicode)

        def __init__(self, **kwargs):
            try:
                params = CoopTableParams(kwargs)
                self.entry_id = params.entry_id
                self.date = params.date
                self.client_type = params.coop_type
                self.tasks = params.tasks
                self.notes = params.notes
            except KeyError:
                pass

        @classmethod
        def set_table_name(cls, value: str):
            cls.__tablename__ = value

        def __repr__(self):
            return f"Coop_table_{self.client_id}"

    return CoopTableDef, CoopBaseDef
