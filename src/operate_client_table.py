from default_table import DefaultTable
from basic_defs import ClientType
from client_table_schema import client_table_suffix, create_client_table
from client_table_params import ClientTableParams
from logger import log_settings
app_log = log_settings()


class OperateClientTable(DefaultTable):

    def __init__(self, cid: int, name: str, surname: str) -> None:
        super().__init__(cid=cid)
        self._table_name = client_table_suffix + name + self._separator + surname + self._separator + str(cid)
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
    OperateClientTable(cid=2,
                       name="Name",
                       surname="Surname").insert_entry(client_type=ClientType.MZ,
                                                       date="2022-08-02",
                                                       tasks="to do",
                                                       notes="notes")
    resp = OperateClientTable(cid=2,
                              name="Name",
                              surname="Surname").select_all()
    for item in resp:
        print(f"{item.entry_id} - {item.client_type} - {item.date} - "
              f"{item.tasks} - {item.notes}")
