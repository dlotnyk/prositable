from typing import Optional, List, Tuple
from basic_defs import KnownFrom, Cities
from local_db import LocalDb
from datetime import datetime
from datetime import date
from table_schemas import MainTable, main_table_name, Base
from logger import log_settings
app_log = log_settings()


def chaining(fun):
    def inner(*args, **kwargs):
        inst = LocalDb()
        inst.open_session()
        fun(*args, **kwargs)
        inst.close_session()
        inst.close_engine()
    return inner


class OperateMainTable:
    _table_name = main_table_name

    def __init__(self) -> None:
        self._dbase = None

    def _open(self) -> None:
        self._dbase = LocalDb()
        self._dbase.open_session()

    def _close(self) -> None:
        self._dbase.close_session()
        self._dbase.close_engine()

    def select_all(self) -> Optional[List]:
        self._open()
        if self._dbase and self._dbase.session:
            resp = self._dbase.session.query(MainTable).all()
            self._close()
            return resp
        return None

    @staticmethod
    def _calculate_age(born):
        today = datetime.today()
        try:
            birthday = born.replace(year=today.year)
        except ValueError:  # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year, month=born.month + 1, day=1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

    def _get_birth(self, dbirth: str) -> Tuple[Optional[datetime], Optional[int]]:
        if dbirth:
            born = datetime.strptime(dbirth, "%Y-%m-%d")
            age = self._calculate_age(born)
            return born, age
        else:
            return None, None

    def insert_entry(self, client_id: int, name: str, surname: str,
                     known_from: KnownFrom, phone=None, email=None,
                     birth=None, age=None, city=None) -> None:
        try:
            birthday, c_age = self._get_birth(birth)
            if c_age:
                age = c_age
            data = MainTable(client_id=client_id,
                             name=name,
                             surname=surname,
                             known_from=known_from,
                             phone=phone,
                             email=email,
                             birth=birthday,
                             age=age,
                             city=city)
            self._open()
            if self._dbase and self._dbase.session:
                self._dbase.session.add(data)
                self._dbase.session.commit()
                app_log.debug(f"Entry inserted to `{MainTable.__tablename__}`")
        except Exception as ex:
            app_log.error(f"Can not insert into {MainTable.__tablename__}: {ex}")


if __name__ == "__main__":
    OperateMainTable().insert_entry(client_id=2, name="test_name", surname="test_surname",
                                    age=11,
                                    known_from=KnownFrom.university, city=Cities.Kosice)
    resp = OperateMainTable().select_all()
    print(resp[0].surname)
