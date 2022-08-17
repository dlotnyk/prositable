from typing import Optional, Tuple, Dict
from schemas.client_table_schema import client_table_suffix
from schemas.coop_table_schema import coop_table_suffix
from db_create.local_db import ClientTableDb, CoopTableDb
from logger import log_settings
from defs.update_settings import UpdateSettings
app_log = log_settings()


class UpdateTableNames:
    _separator = "_"

    def __init__(self, settings: UpdateSettings) -> None:
        self._settings = settings
        self._rename_coop_table()
        self._rename_client_table()

    def __repr__(self) -> str:
        return "UpdateTableNames"

    def _get_old_suffix(self) -> str:
        return self._settings.old_name + self._separator + self._settings.old_surname + self._separator + str(self._settings.old_id)

    def _get_new_suffix(self) -> str:
        return self._settings.new_name + self._separator + self._settings.new_surname + self._separator + str(self._settings.new_id)

    def _get_old_coop_name(self) -> str:
        return coop_table_suffix + self._get_old_suffix()

    def _get_new_coop_name(self) -> str:
        return coop_table_suffix + self._get_new_suffix()

    def _get_old_client_name(self) -> str:
        return client_table_suffix + self._get_old_suffix()

    def _get_new_client_name(self) -> str:
        return client_table_suffix + self._get_new_suffix()

    def _rename_coop_table(self):
        inst = CoopTableDb(cid=self._settings.old_id,
                           name=self._settings.old_name,
                           surname=self._settings.old_surname)
        inst.rename_table(old_name=self._get_old_coop_name(), new_name=self._get_new_coop_name())
        inst.close_engine()

    def _rename_client_table(self):
        inst = ClientTableDb(cid=self._settings.old_id,
                             name=self._settings.old_name,
                             surname=self._settings.old_surname)
        inst.rename_table(old_name=self._get_old_client_name(), new_name=self._get_new_client_name())
        inst.close_engine()


if __name__ == "__main__":
    a = ['client_history_mm_sa_2', 'coop_history_mm_sa_2', 'main_table']
    b = UpdateSettings("update_name", (2, "ma", ), a)
    UpdateTableNames(b)
