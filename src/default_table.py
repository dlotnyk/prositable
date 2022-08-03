from typing import Optional, List, Tuple
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError, OperationalError

from table_schemas import Base
from local_db import LocalDb
from logger import log_settings
app_log = log_settings()


class DefaultTable:
    _separator = "_"
    _table_name = ""
    _table_base: Optional[Base] = None

    def __init__(self, cid=None):
        self._cid = cid
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

    def _insert_data(self, data):
        try:
            self._open()
            if self._dbase and self._dbase.session:
                try:
                    self._dbase.session.add(data)
                    self._dbase.session.commit()
                    app_log.info(f"Entry inserted to `{self._table_base.__tablename__}`")
                except OperationalError as aa:
                    app_log.info(f"{aa}")
                except IntegrityError as ab:
                    st = str(ab)
                    app_log.info(f"Can not insert into {self._table_base.__tablename__}: `{st[0:100]}`")
                except Exception as ex1:
                    app_log.error(f"Can not insert into {self._table_base.__tablename__}: {ex1}")
                finally:
                    self._close()
        except Exception as ex:
            app_log.error(f"Can not insert into {self._table_base.__tablename__}: {ex}")

    def select_all(self) -> Optional[List]:
        try:
            self._open()
            if self._dbase and self._dbase.session and self.table_base:
                resp = self._dbase.session.query(self.table_base).all()
                return resp
            return list()
        except OperationalError as oe:
            oo = str(oe)
            app_log.error(f"{oo}")
            return list()
        finally:
            self._close()

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

