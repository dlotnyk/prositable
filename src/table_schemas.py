import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

from basic_defs import KnownFrom, Cities, Education, WorkType, FamilyStatus
Base = declarative_base()

main_table_name = "main_table"


class MainTable(Base):
    """
    The main Table
    """
    __tablename__ = main_table_name
    client_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    surname = db.Column(db.Unicode, nullable=False)
    known_from = db.Column(db.Enum(KnownFrom), nullable=False)
    phone = db.Column(db.Integer, nullable=True, unique=True)
    address = db.Column(db.Unicode, nullable=True)
    education = db.Column(db.Enum(Education), nullable=True)
    email = db.Column(db.String, nullable=True, unique=True)
    birth = db.Column(db.Date, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    work_type = db.Column(db.Enum(WorkType), nullable=True)
    family_status = db.Column(db.Enum(FamilyStatus), nullable=True)
    title = db.Column(db.String, nullable=True)
    city = db.Column(db.Enum(Cities), nullable=True)

    def __init__(self, client_id: int, name: str, surname: str, known_from: KnownFrom, phone=None, address=None,
                 education=None, email=None, birth=None, age=None, work_type=None,
                 family_status=None, title=None, city=None):
        self.client_id = client_id
        self.name = name
        self.surname = surname
        self.known_from = known_from
        self.phone = phone
        self.address = address
        self.education = education
        self.email = email
        self.birth = birth
        self.age = age
        self.work_type = work_type
        self.family_status = family_status
        self.title = title
        self.city = city

    def __repr__(self):
        return "MainTable"
