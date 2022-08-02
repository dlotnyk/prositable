from abc import abstractmethod
import sqlalchemy as db
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError
import os
from typing import Optional
from table_schemas import Base, main_table_name
from client_table_schema import ClientBase, client_table_suffix, create_client_table

from main_table_columns import MainTableColumns, ClientTableColumns
from dbs.db_defs import local_db_name
from logger import log_settings
app_log = log_settings()


class LocalDb:
    """
    local db based of sqlite3
    """
    _db_name = local_db_name
    _table_name = main_table_name

    def __init__(self) -> None:
        self.is_ok = True
        try:
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

    @abstractmethod
    def create_table(self):
        pass

    @abstractmethod
    def add_column(self, column_name: str, column_type: str) -> None:
        pass

    @abstractmethod
    def delete_column(self, column_name: str) -> None:
        pass


class MainTableDb(LocalDb):

    def __init__(self):
        self._table_name = main_table_name
        super().__init__()

    def create_table(self):
        metadata = db.MetaData()
        db.Table(self._table_name, metadata,
                 db.Column(MainTableColumns.c_client_id, db.Integer, primary_key=True),
                 db.Column(MainTableColumns.c_name, db.Unicode, nullable=False),
                 db.Column(MainTableColumns.c_surname, db.Unicode, nullable=False),
                 db.Column(MainTableColumns.c_known_from, db.Enum, nullable=False),
                 db.Column(MainTableColumns.c_phone, db.Integer, nullable=True),
                 db.Column(MainTableColumns.c_address, db.Unicode, nullable=True),
                 db.Column(MainTableColumns.c_education, db.Enum, nullable=True),
                 db.Column(MainTableColumns.c_email, db.String, nullable=True),
                 db.Column(MainTableColumns.c_birth, db.Date, nullable=True),
                 db.Column(MainTableColumns.c_age, db.Integer, nullable=True),
                 db.Column(MainTableColumns.c_income, db.Float, nullable=True),
                 db.Column(MainTableColumns.c_income2, db.Float, nullable=True),
                 db.Column(MainTableColumns.c_work_type, db.Enum, nullable=True),
                 db.Column(MainTableColumns.c_family_status, db.Enum, nullable=True),
                 db.Column(MainTableColumns.c_children, db.Float, nullable=True),
                 db.Column(MainTableColumns.c_title, db.String, nullable=True),
                 db.Column(MainTableColumns.c_city, db.Enum, nullable=True)
                 )
        try:
            Base.metadata.create_all(self.db_engine)
            app_log.debug(f"Table `{self._table_name}` was created")
        except Exception as ex:
            self.is_ok = False
            app_log.error(f"Can not create table: `{ex}`")

    def add_column(self, column_name, column_type):
        try:
            self._db_engine.execute(f"ALTER TABLE {self._table_name} "
                                    f"ADD COLUMN {column_name} {column_type}")
            app_log.info(f"Column `{column_name}` created")
        except OperationalError:
            app_log.info(f"Column `{column_name}` already exists")
        except Exception as ex:
            app_log.error(f"Column not created: {ex}")

    def drop_column(self, column_name):
        try:
            self._db_engine.execute(f"ALTER TABLE {self._table_name} "
                                    f"DROP COLUMN {column_name}")
            app_log.info(f"Column `{column_name}` is dropped")
        except OperationalError as ee:
            app_log.info(f"{ee}")
        except Exception as ex:
            app_log.error(f"Column not dropped: {ex}")


class ClientTableDb(LocalDb):

    def __init__(self, client_id: int):
        self._id = client_id
        self._table_name = client_table_suffix + str(client_id)
        create_client_table(self._table_name)
        super().__init__()

    def create_table(self):
        metadata = db.MetaData()
        db.Table(self._table_name, metadata,
                 db.Column(ClientTableColumns.c_entry_id, db.Integer, db.ForeignKey('client.entry_id'), primary_key=True, autoincrement=True,
                           ),
                 db.Column(ClientTableColumns.c_date, db.Date, nullable=False),
                 db.Column(ClientTableColumns.c_client_type, db.Enum),
                 db.Column(ClientTableColumns.c_tasks, db.Unicode),
                 db.Column(ClientTableColumns.c_notes, db.Unicode)
                 )
        try:
            ClientBase.metadata.create_all(self.db_engine)
            app_log.debug(f"Table `{self._table_name}` was created")
        except Exception as ex:
            self.is_ok = False
            app_log.error(f"Can not create table: `{ex}`")

    def add_column(self, column_name: str, column_type: str) -> None:
        pass

    def delete_column(self, column_name: str) -> None:
        pass


if __name__ == "__main__":
    # a = MainTableDb()
    # a.create_table()
    # a.drop_column("income3")
    # a.add_column("income4", "FLOAT")
    # a.close_engine()
    b = ClientTableDb(2)
    b.create_table()
    b.close_engine()