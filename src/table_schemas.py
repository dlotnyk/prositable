import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

from basic_defs import KnownFrom, Cities, Education, WorkType, FamilyStatus
from main_table_params import MainTableParams
Base = declarative_base()

main_table_name = "main_table"
coop_table_suffix = "coop_history_"


class MainTable(Base):
    """
    The main Table
    """
    __tablename__ = main_table_name
    client_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    surname = db.Column(db.Unicode, nullable=False)
    known_from = db.Column(db.Enum(KnownFrom), nullable=False)
    first_contact = db.Column(db.Date, nullable=True)
    phone = db.Column(db.Integer, nullable=True, unique=True)
    address = db.Column(db.Unicode, nullable=True)
    education = db.Column(db.Enum(Education), nullable=True)
    email = db.Column(db.String, nullable=True, unique=True)
    birth = db.Column(db.Date, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    work_type = db.Column(db.Enum(WorkType), nullable=True)
    family_status = db.Column(db.Enum(FamilyStatus), nullable=True)
    children = db.Column(db.Float, nullable=True)
    title = db.Column(db.String, nullable=True)
    city = db.Column(db.Enum(Cities), nullable=True)
    income = db.Column(db.Float, nullable=True)
    income2 = db.Column(db.Float, nullable=True)

    def __init__(self, **kwargs):
        try:
            params = MainTableParams(kwargs)
            self.client_id = params.client_id
            self.name = params.name
            self.surname = params.surname
            self.known_from = params.known_from
            self.first_contact = params.first_contact
            self.phone = params.phone
            self.address = params.address
            self.education = params.education
            self.email = params.email
            self.birth = params.birth
            self.age = params.age
            self.work_type = params.work_type
            self.family_status = params.family_status
            self.title = params.title
            self.city = params.city
            self.children = params.children
            self.income = params.income
            self.income2 = params.income2
        except KeyError:
            pass

    def __repr__(self):
        return "MainTable"
