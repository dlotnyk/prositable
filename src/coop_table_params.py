from typing import Dict
from datetime import date
from main_table_columns import CoopTableColumns


class CoopTableParams:

    def __init__(self, kwargs: Dict) -> None:
        self._params = kwargs
        self._keys = set(self._params.keys())

    @property
    def entry_id(self) -> int:
        return self._params.get(CoopTableColumns.c_entry_id, None)

    @property
    def coop_type(self) -> str:
        return self._params.get(CoopTableColumns.c_coop_type, None)

    @property
    def date(self) -> date:
        return self._params.get(CoopTableColumns.c_date, None)

    @property
    def tasks(self) -> str:
        return self._params.get(CoopTableColumns.c_tasks, None)

    @property
    def notes(self) -> str:
        return self._params.get(CoopTableColumns.c_notes, None)
