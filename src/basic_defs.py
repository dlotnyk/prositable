from enum import Enum


class KnownFrom(Enum):
    relatives = 0
    school = 1
    work = 2
    university = 3


class Cities(Enum):
    Kosice = 0
    Presov = 1


class Education(Enum):
    higher = 0
    middle = 1
    maturita = 2


class WorkType(Enum):
    worker = 0
    business = 1


class FamilyStatus(Enum):
    single = 0
    married = 1
    divorced = 2
    unkhown = 3
