from typing import Optional, List, Tuple
from datetime import datetime, date

from table_schemas import Base
from local_db import LocalDb


class DefaultTable:
    _table_name = ""
    _table_base: Optional[Base] = None

    def __init__(self):
        self._dbase: Optional[LocalDb] = None

    @property
    def table_base(self) -> Optional[Base]:
        return self._table_base

    def _open(self) -> None:
        self._dbase = LocalDb()
        self._dbase.open_session()

    def _close(self) -> None:
        self._dbase.close_session()
        self._dbase.close_engine()

    def select_all(self) -> Optional[List]:
        self._open()
        if self._dbase and self._dbase.session and self.table_base:
            resp = self._dbase.session.query(self.table_base).all()
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

    def _get_birth(self, dbirth: str) -> Tuple[Optional[date], Optional[int]]:
        if dbirth:
            born = datetime.strptime(dbirth, "%Y-%m-%d")
            age = self._calculate_age(born)
            return born, age
        else:
            return None, None

