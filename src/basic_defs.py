from enum import Enum


class TableDefs:
    c_client_prefix = "client_history_"
    c_coop_prefix = "coop_history_"


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


class ClientType(Enum):
    MZ = 0
    DPK = 1
    DEK = 2
    DDNK = 3
    DNK = 4


class CoopType(Enum):
    MZ = 0
    DPS = 1
    DES = 2
    DDNS = 3
    DNS = 4
