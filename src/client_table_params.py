from typing import Dict
from datetime import date
from main_table_columns import ClientTableColumns


class ClientTableParams:

    def __init__(self, kwargs: Dict) -> None:
        self._params = kwargs
        self._keys = set(self._params.keys())

    @property
    def entry_id(self) -> int:
        return self._params.get(ClientTableColumns.c_entry_id, None)

    @property
    def client_type(self) -> int:
        return self._params.get(ClientTableColumns.c_client_type, None)

    @property
    def date(self) -> int:
        return self._params.get(ClientTableColumns.c_date, None)

    @property
    def tasks(self) -> int:
        return self._params.get(ClientTableColumns.c_tasks, None)

    @property
    def notes(self) -> int:
        return self._params.get(ClientTableColumns.c_notes, None)
