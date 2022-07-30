import sqlalchemy as db
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
import os
from typing import Optional
from table_schemas import Base, main_table_name

from dbs.db_defs import local_db_name
from logger import log_settings
app_log = log_settings()


class LocalDb:
    """
    local db based of sqlite3
    """

    def __init__(self) -> None:
        self.is_ok = True
        try:
            self._main_table_name = main_table_name
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
            self.is_ok = False

    @property
    def session(self) -> Optional[Session]:
        return self._session

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
            self.is_ok = False
            app_log.error(f"Can not create table: `{ex}`")

    def open_session(self):
        """
        Opens the local db
        """
        if self.is_ok:
            try:
                sess = sessionmaker(bind=self.db_engine)
                self._session = sess()
                app_log.debug(f"Session creates for: `{self._db_name}` ")
            except Exception as ex:
                self.is_ok = False
                app_log.error(f"Can not create session: {ex}")

    def close_session(self):
        """
        Close connection to db
        """
        try:
            if self._session is not None and self.is_ok:
                self._session.close()
                app_log.debug(f"Session `{self._db_name}` closed ")
        except Exception as ex:
            self.is_ok = False
            app_log.error(f"Can not close session: {ex}")

    def close_engine(self):
        """
        Close the db engine
        """
        if self.is_ok:
            try:
                self.db_engine.dispose()
                app_log.debug("db Engine disposed ")
            except Exception as ex:
                self.is_ok = False
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