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
