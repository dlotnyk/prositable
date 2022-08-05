from db_create.default_table import DefaultTable
from defs.basic_defs import CoopType
from schemas.coop_table_schema import coop_table_suffix, create_coop_table
from defs.coop_table_params import CoopTableParams
from logger import log_settings
app_log = log_settings()


class OperateCoopTable(DefaultTable):

    def __init__(self, cid: int, name: str, surname: str) -> None:
        super().__init__(cid=cid)
        self._table_name = coop_table_suffix + name + self._separator + surname + self._separator + str(cid)
        self._table_base, _ = create_coop_table(self._table_name)

    def insert_entry(self, **kwargs) -> None:
        params = CoopTableParams(kwargs)
        entry_id = params.entry_id
        coop_type = params.coop_type
        cdate = params.date
        tasks = params.tasks
        notes = params.notes
        date, _ = self._get_birth(cdate)

        data = self._table_base(entry_id=entry_id,
                                coop_type=coop_type,
                                date=date,
                                tasks=tasks,
                                notes=notes)
        self._insert_data(data)


if __name__ == "__main__":
    OperateCoopTable(cid=2,
                     name="Name",
                     surname="Surname").insert_entry(coop_type=CoopType.MZ,
                                                     date="2022-08-02",
                                                     tasks="to do",
                                                     notes="notes")
    resp = OperateCoopTable(cid=2,
                            name="Name",
                            surname="Surname").select_all()
    for item in resp:
        print(f"{item.entry_id} - {item.coop_type} - {item.date} - "
              f"{item.tasks} - {item.notes}")
