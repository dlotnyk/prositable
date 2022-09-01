from typing import Dict, Optional
from datetime import date
from defs.basic_defs import KnownFrom, Cities, Education, WorkType, FamilyStatus
from defs.main_table_columns import MainTableColumns


class MainTableParams:

    def __init__(self, kwargs: Dict) -> None:
        self._params = kwargs
        self._keys = set(self._params.keys())

    @property
    def client_id(self) -> int:
        return self._params.get(MainTableColumns.c_client_id, None)

    @property
    def name(self) -> str:
        resp = self._params.get(MainTableColumns.c_name, None)
        if resp:
            return resp
        else:
            raise KeyError(f"{MainTableColumns.c_name} not defined")

    @property
    def surname(self) -> str:
        resp = self._params.get(MainTableColumns.c_surname, None)
        if resp:
            return resp
        else:
            raise KeyError(f"{MainTableColumns.c_surname} not defined")

    @property
    def rc(self) -> int:
        return self._params.get(MainTableColumns.c_rc, None)

    @property
    def known_from(self) -> KnownFrom:
        resp = self._params.get(MainTableColumns.c_known_from, None)
        if resp:
            return resp
        else:
            raise KeyError(f"{MainTableColumns.c_known_from} not defined")

    @property
    def first_contact(self) -> Optional[date]:
        return self._params.get(MainTableColumns.c_first_contact, None)

    @property
    def phone(self) -> Optional[str]:
        return self._params.get(MainTableColumns.c_phone, None)

    @property
    def address(self) -> Optional[str]:
        return self._params.get(MainTableColumns.c_address, None)

    @property
    def education(self) -> Optional[Education]:
        return self._params.get(MainTableColumns.c_education, None)

    @property
    def email(self) -> Optional[str]:
        return self._params.get(MainTableColumns.c_email, None)

    @property
    def birth(self) -> Optional[date]:
        return self._params.get(MainTableColumns.c_birth, None)

    @property
    def age(self) -> Optional[int]:
        return self._params.get(MainTableColumns.c_age, None)

    @property
    def work_type(self) -> Optional[WorkType]:
        return self._params.get(MainTableColumns.c_work_type, None)

    @property
    def family_status(self) -> Optional[FamilyStatus]:
        return self._params.get(MainTableColumns.c_family_status, None)

    @property
    def title(self) -> Optional[str]:
        return self._params.get(MainTableColumns.c_title, None)

    @property
    def city(self) -> Optional[Cities]:
        return self._params.get(MainTableColumns.c_city, None)

    @property
    def children(self) -> Optional[float]:
        return self._params.get(MainTableColumns.c_children, None)

    @property
    def income(self) -> Optional[float]:
        return self._params.get(MainTableColumns.c_income, None)

    @property
    def income2(self) -> Optional[float]:
        return self._params.get(MainTableColumns.c_income2, None)

    @property
    def trvaly_pobyt(self) -> Optional[str]:
        return self._params.get(MainTableColumns.c_trvaly_pobyt, None)

    @property
    def nationality(self) -> Optional[str]:
        return self._params.get(MainTableColumns.c_nationality, None)

    @property
    def op_number(self) -> Optional[str]:
        return self._params.get(MainTableColumns.c_op_number, None)


if __name__ == "__main__":
    params = {"client_id": 111}
    a = MainTableParams(params)
    print(a.client_id)
