from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from typing import Optional, List, Tuple

from default_table import DefaultTable
from basic_defs import KnownFrom, Cities
from table_schemas import MainTable, main_table_name
from logger import log_settings
app_log = log_settings()


class OperateMainTable(DefaultTable):
    _table_name = main_table_name
    _table_base = MainTable

    def __init__(self) -> None:
        super().__init__()

    def insert_entry(self, client_id: int, name: str, surname: str,
                     known_from: KnownFrom, phone=None, email=None, address=None,
                     education=None, birth=None, age=None, city=None) -> None:
        try:
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
                                    city=city)
            self._open()
            if self._dbase and self._dbase.session:
                try:
                    self._dbase.session.add(data)
                    self._dbase.session.commit()
                    app_log.info(f"Entry inserted to `{self._table_base.__tablename__}`")
                except IntegrityError:
                    app_log.info(f"Can not insert into {self._table_base.__tablename__}: id already exists")
                except Exception as ex1:
                    app_log.error(f"Can not insert into {self._table_base.__tablename__}: {ex1}")
                finally:
                    self._close()
        except Exception as ex:
            app_log.error(f"Can not insert `{client_id}` into {self._table_base.__tablename__}: {ex}")

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
    OperateMainTable().insert_entry(client_id=1, name="test_name", surname="test_surname",
                                    birth="2008-08-11",
                                    known_from=KnownFrom.university, city=Cities.Kosice)
    OperateMainTable().delete_entry(0)
    resp = OperateMainTable().select_all()
    for item in resp:
        print(f"{item.client_id} - {item.name} - {item.surname} - {item.known_from} - {item.birth} - {item.age} - "
              f"{item.phone} - {item.city}")
