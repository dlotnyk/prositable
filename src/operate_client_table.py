from db_create.default_table import AuxTable
from defs.basic_defs import ClientType
from schemas.client_table_schema import client_table_suffix, create_client_table
from defs.client_table_params import ClientTableParams
from logger import log_settings
app_log = log_settings()


class OperateClientTable(AuxTable):
    _tab_prefix = client_table_suffix

    def __init__(self, cid: int, name: str, surname: str) -> None:
        super().__init__(cid=cid, name=name, surname=surname)
        self._table_base, _ = create_client_table(self._table_name)

    def insert_entry(self, **kwargs) -> None:
        params = ClientTableParams(kwargs)
        entry_id = params.entry_id
        client_type = params.client_type
        cdate = params.date
        tasks = params.tasks
        notes = params.notes
        date, _ = self._get_birth(cdate)

        data = self._table_base(entry_id=entry_id,
                                client_type=client_type,
                                date=date,
                                tasks=tasks,
                                notes=notes)
        self._insert_data(data)


if __name__ == "__main__":
    # OperateClientTable(cid=3,
    #                    name="sm",
    #                    surname="rk").insert_entry(client_type=ClientType.MZ,
    #                                                    date="2022-08-02",
    #                                                    tasks="to do",
    #                                                    notes="notes")
    OperateClientTable(cid=3,
                       name="sm",
                       surname="rk").update_client_type(2, ClientType.DNK)

    resp = OperateClientTable(cid=3,
                              name="sm",
                              surname="rk").select_all()
    for item in resp:
        print(f"{item.entry_id} - {item.client_type} - {item.date} - "
              f"{item.tasks} - {item.notes}")
