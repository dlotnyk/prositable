from sqlalchemy.orm.exc import UnmappedInstanceError

from db_create.default_table import DefaultTable
from defs.basic_defs import WorkType, FamilyStatus, Education, KnownFrom, Cities
from schemas.table_schemas import MainTable, main_table_name
from defs.main_table_params import MainTableParams
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
        first_contact = params.first_contact
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
        contact, _ = self._get_birth(first_contact)
        birthday, c_age = self._get_birth(birth)
        if c_age:
            age = c_age
        data = self._table_base(client_id=client_id,
                                name=name,
                                surname=surname,
                                known_from=known_from,
                                first_contact=contact,
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


if __name__ == "__main__":
    OperateMainTable().insert_entry(client_id=2,
                                    name="Name",
                                    surname="Surname",
                                    birth="2008-08-11",
                                    phone=421944123457,
                                    education=Education.higher,
                                    address="some 1",
                                    title="ing",
                                    email="21@11.com",
                                    children=1,
                                    income=1234.4,
                                    income2=11.1,
                                    first_contact="2021-01-19",
                                    work_type=WorkType.worker,
                                    family_status=FamilyStatus.married,
                                    known_from=KnownFrom.university,
                                    city=Cities.Kosice)
    OperateMainTable().delete_entry(0)
    resp = OperateMainTable().select_all()
    for item in resp:
        print(f"{item.client_id} - {item.name} - {item.surname} - {item.known_from} - {item.birth} - {item.age} - "
              f"{item.phone} - {item.city}")

