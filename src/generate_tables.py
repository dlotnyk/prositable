from typing import Optional, List
from tables import OperateMainTable
from local_db import ClientTableDb
from table_schemas import MainTable
from logger import log_settings
app_log = log_settings()


class EntryDetails:
    def __init__(self, cid: int, name: str, surname: str):
        self.cid = cid
        self.name = name
        self.surname = surname


class GenerateClientTables:

    def __init__(self):
        self._main_table_inst = OperateMainTable()
        self._client_table_db: Optional[ClientTableDb] = None
        self._details_list: List[EntryDetails] = list()
        self._get_main_table_entries()

    def _get_main_table_entries(self):
        entries_list: List[MainTable] = self._main_table_inst.select_all()
        if entries_list:
            for entry in entries_list:
                self._details_list.append(EntryDetails(cid=entry.client_id,
                                                       name=entry.name,
                                                       surname=entry.surname))

    @property
    def details_list(self) -> List[EntryDetails]:
        return self._details_list

    def create_client_tables(self) -> None:
        if self._details_list:
            for entry in self._details_list:
                try:
                    cl_table = ClientTableDb(client_id=entry.cid,
                                             name=entry.name,
                                             surname=entry.surname)
                    cl_table.create_table()
                    app_log.debug(f"Table created id: {entry.cid}")
                except Exception as ex:
                    app_log.info(f"Can not crate table: {entry.cid} - {entry.name} - "
                                 f"{entry.surname}: {ex}")


if __name__ == "__main__":
    a = GenerateClientTables()
    for item in a.details_list:
        print(f"{item.cid} - {item.name} - {item.surname}")
    a.create_client_tables()
