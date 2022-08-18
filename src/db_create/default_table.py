from typing import Optional, List, Tuple
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError, OperationalError

from schemas.table_schemas import Base
from defs.basic_defs import ClientType, CoopType
from defs.main_table_columns import AuxTableColumns, ClientTableColumns, CoopTableColumns
from db_create.local_db import LocalDb
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
        except ValueError:
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

    def _select_id(self) -> List:
        try:
            self._open()
            if self._dbase and self._dbase.session and self.table_base:
                resp = self._dbase.session.query(self.table_base.entry_id).all()
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


class AuxTable(DefaultTable):
    _tab_prefix = ""

    def __init__(self, cid: int, name: str, surname: str) -> None:
        super().__init__(cid=cid)
        self._table_name = self._tab_prefix + name + self._separator + surname + self._separator + str(cid)

    def execute_update(func):
        def inner(self, *args, **kwargs):
            self._open()
            try:
                cid = args[0]
                if self._is_valid_id(cid):
                    func(self, *args, **kwargs)
                    self._dbase.session.commit()
                    app_log.info(f"Update of `{self._table_base.__tablename__}`")
                else:
                    app_log.info(f"`{cid}` is not in {self._table_base.__tablename__}")
            except Exception as ex:
                app_log.error(f"Can not updated from {self._table_base.__tablename__}: {ex}")
            finally:
                self._close()
        return inner

    @execute_update
    def update_date(self, entry_id: int, ndate: str):
        hday, _ = self._get_birth(ndate)
        self._dbase.session.query(self._table_base).filter(self._table_base.entry_id == entry_id). \
            update({AuxTableColumns.c_date: hday}, synchronize_session="fetch")

    @execute_update
    def update_notes(self, entry_id: int, note: str):
        self._dbase.session.query(self._table_base).filter(self._table_base.entry_id == entry_id). \
            update({AuxTableColumns.c_notes: note}, synchronize_session="fetch")

    @execute_update
    def update_tasks(self, entry_id: int, task: str):
        self._dbase.session.query(self._table_base).filter(self._table_base.entry_id == entry_id). \
            update({AuxTableColumns.c_tasks: task}, synchronize_session="fetch")

    @execute_update
    def update_coop_type(self, entry_id: int, ctype: CoopType):
        self._dbase.session.query(self._table_base).filter(self._table_base.entry_id == entry_id). \
            update({CoopTableColumns.c_coop_type: ctype}, synchronize_session="fetch")

    @execute_update
    def update_client_type(self, entry_id: int, ctype: ClientType):
        self._dbase.session.query(self._table_base).filter(self._table_base.entry_id == entry_id). \
            update({ClientTableColumns.c_client_type: ctype}, synchronize_session="fetch")
