from sqlalchemy.orm.exc import UnmappedInstanceError

from default_table import DefaultTable
from basic_defs import ClientType
from table_schemas import MainTable, main_table_name
from client_table_schema import client_table_suffix, create_client_table
from main_table_params import MainTableParams
from client_table_params import ClientTableParams
from logger import log_settings
app_log = log_settings()


class OperateMainTable(DefaultTable):
    _table_name = main_table_name
    _table_base = MainTable

    def __init__(self) -> None:
        super().__init__()

    def insert_entry(self, **kwargs) -> None:
        params = MainTableParams(kwargs)
        client_id = params.client_id
        name = params.name
        surname = params.surname
        known_from = params.known_from
        phone = params.phone
        email = params.email
        address = params.address
        education = params.education
        birth = params.birth
        age = params.age
        work_type = params.work_type
        family_status = params.family_status
        title = params.title
        city = params.city
        children = params.children
        income = params.income
        income2 = params.income2
        birthday, c_age = self._get_birth(birth)
        if c_age:
            age = c_age
        data = self._table_base(client_id=client_id,
                                name=name,
                                surname=surname,
                                known_from=known_from,
                                phone=phone,
                                address=address,
                                education=education,
                                email=email,
                                birth=birthday,
                                age=age,
                                work_type=work_type,
                                family_status=family_status,
                                children=children,
                                income=income,
                                income2=income2,
                                title=title,
                                city=city)
        self._insert_data(data)

    def delete_entry(self, client_id: int) -> None:
        try:
            self._open()
            obj = self._dbase.session.query(self._table_base).filter(self._table_base.client_id == client_id).first()
            self._dbase.session.delete(obj)
            self._dbase.session.commit()
            app_log.info(f"Client_id `{client_id}` deleted from `{self._table_base.__tablename__}`")
        except UnmappedInstanceError:
            app_log.info(f"Client_id `{client_id}` does not exists")
        except Exception as ex:
            app_log.error(f"Can not deleted `{client_id}` from {self._table_base.__tablename__}: {ex}")
        finally:
            self._close()


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
    # OperateMainTable().insert_entry(client_id=2, name="test_name", surname="test_surname",
    #                                 birth="2008-08-11", phone=421944123457, education=Education.higher,
    #                                 address="some 1", title="ing", email="21@11.com", children=1,
    #                                 income=1234.4, income2=11.1,
    #                                 work_type=WorkType.worker, family_status=FamilyStatus.married,
    #                                 known_from=KnownFrom.university, city=Cities.Kosice)
    # OperateMainTable().delete_entry(0)
    # resp = OperateMainTable().select_all()
    # for item in resp:
    #     print(f"{item.client_id} - {item.name} - {item.surname} - {item.known_from} - {item.birth} - {item.age} - "
    #           f"{item.phone} - {item.city}")
    #
    OperateClientTable(cid=2,
                       name="test_name",
                       surname="test_surname").insert_entry(client_type=ClientType.mz, date="2022-08-02",
                                      tasks="to do", notes="notes")
    resp = OperateClientTable(cid=0,
                              name="name",
                              surname="surname").select_all()
    for item in resp:
        print(f"{item.entry_id} - {item.client_type} - {item.date} - "
              f"{item.tasks} - {item.notes}")
