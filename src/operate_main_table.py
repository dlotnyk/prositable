from sqlalchemy.orm.exc import UnmappedInstanceError
from typing import List, Tuple, Dict
from sqlalchemy.exc import OperationalError

from db_create.default_table import DefaultTable
from defs.main_table_columns import MainTableColumns
from defs.basic_defs import WorkType, FamilyStatus, Education, KnownFrom, Cities
from schemas.table_schemas import MainTable, main_table_name
from defs.main_table_params import MainTableParams
from logger import log_settings
app_log = log_settings()


class OperateMainTable(DefaultTable):
    _table_name = main_table_name
    _table_base = MainTable

    def __init__(self) -> None:
        DefaultTable().__init__()

    def _select_id(self) -> List:
        try:
            self._open()
            if self._dbase and self._dbase.session and self.table_base:
                resp = self._dbase.session.query(self.table_base.client_id).all()
                return [i[0] for i in resp]
            return list()
        except OperationalError as oe:
            oo = str(oe)
            app_log.error(f"{oo}")
            return list()
        finally:
            self._close()

    def _is_valid_id(self, cid: int) -> bool:
        return cid in self._select_id()

    @staticmethod
    def _is_rename(args: Tuple) -> bool:
        try:
            return args[2] is True
        except IndexError:
            return False

    def execute_update(func):
        def inner(self, *args, **kwargs):
            self._open()
            is_fine = True
            try:
                cid = args[0]
                print(self._dbase.get_table_names())
                if self._is_valid_id(cid):
                    func(self, *args, **kwargs)
                    self._dbase.session.commit()
                    app_log.info(f"Update of `{self._table_base.__tablename__}`")
                else:
                    is_fine = False
                    app_log.info(f"`{cid}` is not in {self._table_base.__tablename__}")
            except Exception as ex:
                is_fine = False
                app_log.error(f"Can not updated from {self._table_base.__tablename__}: {ex}")
            finally:
                self._close()
        return inner

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
        self._open()
        try:
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

    @execute_update
    def update_city(self, client_id: int, city: Cities) -> None:
        self._dbase.session.query(self._table_base).filter(self._table_base.client_id == client_id). \
            update({MainTableColumns.c_city: city}, synchronize_session="fetch")

    @execute_update
    def update_title(self, client_id: int, title: str) -> None:
        self._dbase.session.query(self._table_base).filter(self._table_base.client_id == client_id). \
            update({MainTableColumns.c_title: title}, synchronize_session="fetch")

    @execute_update
    def update_children(self, client_id: int, children: float) -> None:
        self._dbase.session.query(self._table_base).filter(self._table_base.client_id == client_id). \
            update({MainTableColumns.c_children: children}, synchronize_session="fetch")

    @execute_update
    def update_income(self, client_id: int, income: float) -> None:
        self._dbase.session.query(self._table_base).filter(self._table_base.client_id == client_id). \
            update({MainTableColumns.c_income: income}, synchronize_session="fetch")

    @execute_update
    def update_income2(self, client_id: int, income2: float) -> None:
        self._dbase.session.query(self._table_base).filter(self._table_base.client_id == client_id). \
            update({MainTableColumns.c_income2: income2}, synchronize_session="fetch")

    @execute_update
    def update_family_status(self, client_id: int, status: FamilyStatus) -> None:
        self._dbase.session.query(self._table_base).filter(self._table_base.client_id == client_id). \
            update({MainTableColumns.c_family_status: status}, synchronize_session="fetch")

    @execute_update
    def update_work_type(self, client_id: int, work_type: WorkType) -> None:
        self._dbase.session.query(self._table_base).filter(self._table_base.client_id == client_id). \
            update({MainTableColumns.c_work_type: work_type}, synchronize_session="fetch")

    @execute_update
    def update_age(self, client_id: int, age: int) -> None:
        self._dbase.session.query(self._table_base).filter(self._table_base.client_id == client_id). \
            update({MainTableColumns.c_age: age}, synchronize_session="fetch")

    @execute_update
    def update_birth(self, client_id: int, birth: str) -> None:
        birthday, c_age = self._get_birth(birth)
        self._dbase.session.query(self._table_base).filter(self._table_base.client_id == client_id). \
            update({MainTableColumns.c_age: c_age}, synchronize_session="fetch")
        self._dbase.session.query(self._table_base).filter(self._table_base.client_id == client_id). \
            update({MainTableColumns.c_birth: birthday}, synchronize_session="fetch")

    @execute_update
    def update_email(self, client_id: int, email: str) -> None:
        self._dbase.session.query(self._table_base).filter(self._table_base.client_id == client_id). \
            update({MainTableColumns.c_email: email}, synchronize_session="fetch")

    @execute_update
    def update_education(self, client_id: int, education: Education) -> None:
        self._dbase.session.query(self._table_base).filter(self._table_base.client_id == client_id). \
            update({MainTableColumns.c_education: education}, synchronize_session="fetch")

    @execute_update
    def update_address(self, client_id: int, address: str) -> None:
        self._dbase.session.query(self._table_base).filter(self._table_base.client_id == client_id). \
            update({MainTableColumns.c_address: address}, synchronize_session="fetch")

    @execute_update
    def update_phone(self, client_id: int, phone: str) -> None:
        self._dbase.session.query(self._table_base).filter(self._table_base.client_id == client_id). \
            update({MainTableColumns.c_phone: phone}, synchronize_session="fetch")

    @execute_update
    def update_first_contact(self, client_id: int, contact: str) -> None:
        first, _ = self._get_birth(contact)
        self._dbase.session.query(self._table_base).filter(self._table_base.client_id == client_id). \
            update({MainTableColumns.c_first_contact: first}, synchronize_session="fetch")

    @execute_update
    def update_known_from(self, client_id: int, known: KnownFrom) -> None:
        self._dbase.session.query(self._table_base).filter(self._table_base.client_id == client_id). \
            update({MainTableColumns.c_known_from: known}, synchronize_session="fetch")

    @execute_update
    def update_surname(self, client_id: int, surname: str, rename: bool) -> None:
        self._dbase.session.query(self._table_base).filter(self._table_base.client_id == client_id). \
            update({MainTableColumns.c_surname: surname}, synchronize_session="fetch")

    @execute_update
    def update_name(self, client_id: int, name: str, rename: bool) -> None:
        self._dbase.session.query(self._table_base).filter(self._table_base.client_id == client_id). \
            update({MainTableColumns.c_name: name}, synchronize_session="fetch")

    @execute_update
    def update_id(self, client_id: int, cid: int, rename: bool) -> None:
        self._dbase.session.query(self._table_base).filter(self._table_base.client_id == client_id). \
            update({MainTableColumns.c_client_id: cid}, synchronize_session="fetch")


if __name__ == "__main__":
    OperateMainTable().insert_entry(client_id=2,
                                    name="mm",
                                    surname="sa",
                                    birth="",
                                    phone="",
                                    education=Education.higher,
                                    address="Juzna",
                                    title="PhD",
                                    email="",
                                    children=0,
                                    income=1000,
                                    income2=0,
                                    first_contact="2022-07-29",
                                    work_type=WorkType.worker,
                                    family_status=FamilyStatus.single,
                                    known_from=KnownFrom.university,
                                    city=Cities.Kosice)
    # OperateMainTable().update_title(2, "PhD")
    # OperateMainTable().update_surname(2, "Ann", True)
    # OperateMainTable().update_id(2, 3, True)
    resp = OperateMainTable().select_all()
    for item in resp:
        print(f"{item.client_id} - {item.name} - {item.surname} - {item.known_from} - {item.birth} - {item.age} - "
              f"{item.phone} - {item.city}")
