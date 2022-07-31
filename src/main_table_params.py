from typing import Set, Dict, Optional
from datetime import date
from basic_defs import KnownFrom, Cities, Education, WorkType, FamilyStatus
from main_table_columns import MainTableColumns


class MainTableParams:
    _mandatory_params: Set = {"client_id", "name", "surname", "known_from"}
    _optional_params: Set = {"phone", "address", "education", "email", "birth",
                             "age", "work_type", "family_status", "title", "city"}

    def __init__(self, kwargs: Dict) -> None:
        self._params = kwargs
        self._keys = set(self._params.keys())
        self._check_mandatory()

    @property
    def mandatory_params(self) -> Set:
        return self._mandatory_params

    @property
    def optional_params(self) -> Set:
        return self._optional_params

    @property
    def all_params(self) -> Set:
        return self._mandatory_params.union(self._optional_params)

    def _check_mandatory(self) -> None:
        if self.mandatory_params.issubset(self._keys):
            raise KeyError("Not all mandatory parameters are defined")

    @property
    def client_id(self) -> int:
        resp = self._params.get(MainTableColumns.c_client_id, None)
        if resp:
            return resp
        else:
            raise KeyError(f"{MainTableColumns.c_client_id} not defined")

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
    def known_from(self) -> KnownFrom:
        resp = self._params.get(MainTableColumns.c_known_from, None)
        if resp:
            return resp
        else:
            raise KeyError(f"{MainTableColumns.c_known_from} not defined")

    @property
    def phone(self) -> Optional[int]:
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
