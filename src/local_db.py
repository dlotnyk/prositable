import sqlalchemy as db
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import os
from typing import List, Tuple, Optional

from basic_defs import KnownFrom
from table_schemas import MainTable, main_table_name, Base
from dbs.db_defs import local_db_name
from logger import log_settings
app_log = log_settings()


class LocalDb:
    """
    local db based of sqlite3
    """
    _main_table_name = main_table_name

    def __init__(self) -> None:
        try:
            self._db_name = local_db_name
            self._session: Optional[Session] = None
            cur_path = os.path.dirname(os.getcwd())
            dbs_path = os.path.join(cur_path, "dbs")
            db_path = os.path.join(dbs_path, self._db_name)
            connector = "sqlite:///" + db_path
            self._db_engine: Engine = db.create_engine(connector)
            app_log.debug(f"Engine creates for {self._db_name}")
        except Exception as ex:
            app_log.error(f"Can not create an engine: `{ex}`")
            exit(1)

    @property
    def db_engine(self) -> Engine:
        return self._db_engine

    def create_main_table(self):
        metadata = db.MetaData()
        db.Table(self._main_table_name, metadata,
                 db.Column("client_id", db.Integer, primary_key=True),
                 db.Column("name", db.Unicode, nullable=False),
                 db.Column("surname", db.Unicode, nullable=False),
                 db.Column("known_from", db.Enum, nullable=False),
                 db.Column("phone", db.Integer, nullable=True),
                 db.Column("email", db.String, nullable=True),
                 db.Column("date_of_birth", db.Date, nullable=True),
                 db.Column("age", db.Integer, nullable=True),
                 db.Column("city", db.Enum, nullable=True)
                 )
        try:
            Base.metadata.create_all(self.db_engine)
            app_log.debug(f"Table `{self._main_table_name}` was created")
        except Exception as ex:
            app_log.error(f"Can not create table: `{ex}`")

    def open_session(self):
        """
        Opens the local db
        """
        try:
            sess = sessionmaker(bind=self.db_engine)
            self._session = sess()
            app_log.debug(f"Session creates for: `{self._db_name}` ")
        except Exception as ex:
            app_log.error(f"Can not create session: {ex}")

    def close_session(self):
        """
        Close connection to db
        """
        try:
            if self._session is not None:
                self._session.close()
                app_log.debug(f"Session `{self._db_name}` closed ")
        except Exception as ex:
            app_log.error(f"Can not close session: {ex}")

    def close_engine(self):
        """
        Close the db engine
        """
        try:
            self.db_engine.dispose()
            app_log.debug("db Engine disposed ")
        except Exception as ex:
            app_log.error(f"Engine NOT disposed: {ex}")

    #todo remove to tables classes
    def insert_entry(self, name: str, surname: str):
        try:
            data = MainTable(name=name,
                             surname=surname)
            self._session.add(data)
        except Exception as ex:
            app_log.error(f"Can not insert into main table: {ex}")
        else:
            self._session.commit()
            app_log.debug(f"Data committed to `{MainTable.__tablename__}`")

    @property
    def select_all(self):
        return self._session.query(MainTable).all()


if __name__ == "__main__":
    a = LocalDb()
    a.create_main_table()