from typing import Optional, Tuple, Dict
from schemas.client_table_schema import client_table_suffix
from schemas.coop_table_schema import coop_table_suffix
from db_create.local_db import ClientTableDb, CoopTableDb
from logger import log_settings
app_log = log_settings()


class UpdateTableNames:
    _separator = "_"
    _c_update_id = "update_id"
    _c_cid = "cid"
    _c_old_id = "old_cid"
    _c_new_id = "new_cid"
    _c_old_name = "old_name"
    _c_new_name = "new_name"
    _c_old_surname = "old_surname"
    _c_new_surname = "new_surname"
    _c_update_name = "update_name"
    _c_update_surname = "update_surname"
    _c_func_name = "func_name"
    _c_name = "name"
    _c_surname = "surname"
    _change_func_list: Tuple = (_c_update_id, _c_update_name, _c_update_surname)
    _func_name: Optional[str] = None

    def __init__(self, **kwargs) -> None:
        try:
            self._old_id: Optional[int] = None
            self._new_id: Optional[int] = None
            self._name: Optional[str] = None
            self._old_name: Optional[str] = None
            self._new_name: Optional[str] = None
            self._surname: Optional[str] = None
            self._old_surname: Optional[str] = None
            self._new_surname: Optional[str] = None
            assert kwargs.get(self._c_func_name) is not None, "No func name"
            self._func_name = kwargs.get(self._c_func_name)
            assert self._func_name in self._change_func_list, "Wrong func name"
            self._func_name_id(kwargs)
            self._func_name_name(kwargs)
            self._func_name_surname(kwargs)
        except AssertionError as ex:
            app_log.error(f"{repr(self)}: {ex}")

    def __repr__(self) -> str:
        return "UpdateTableNames"

    def _get_prefix(self, cid: int, name: str, surname: str) -> str:
        return str(name) + self._separator + str(surname) + self._separator + str(cid)

    def _get_names(self, old_cid: int, old_name: str, old_surname: str,
                   new_cid: int, new_name: str, new_surname: str) -> Tuple[str, str]:
        old = self._get_prefix(old_cid, old_name, old_surname)
        new = self._get_prefix(new_cid, new_name, new_surname)
        return old, new

    def _get_coop_name(self,
                       cid: Optional[int],
                       name: Optional[str],
                       surname: Optional[str]) -> str:
        return coop_table_suffix + str(name) + self._separator + str(surname) + self._separator + str(cid)

    def _get_client_name(self,
                         cid: Optional[int],
                         name: Optional[str],
                         surname: Optional[str]) -> str:
        return client_table_suffix + str(name) + self._separator + str(surname) + self._separator + str(cid)

    def _rename_coop_table(self, old_name: str, new_name: str):
        inst = CoopTableDb(cid=self._old_id,
                           name=self._old_name,
                           surname=self._old_surname)
        inst.rename_table(old_name=old_name, new_name=new_name)
        inst.close_engine()

    def _rename_client_table(self, old_name: str, new_name: str):
        inst = ClientTableDb(cid=self._old_id,
                             name=self._old_name,
                             surname=self._old_surname)
        inst.rename_table(old_name=old_name, new_name=new_name)
        inst.close_engine()

    def _func_name_id(self, items: Dict):
        if self._func_name is not None:
            try:
                if self._func_name == self._c_update_id:
                    assert items.get(self._c_old_id) is not None, "old id is missing"
                    assert items.get(self._c_new_id) is not None, "new id is missing"
                    self._old_id = items.get(self._c_old_id)
                    self._new_id = items.get(self._c_new_id)
                    assert self._old_id != self._new_id, "ids can not be equal"
                    self._old_name = items.get(self._c_name, None)
                    self._old_surname = items.get(self._c_surname, None)
                    old, new = self._get_names(old_cid=self._old_id, new_cid=self._new_id,
                                               old_name=self._old_name, new_name=self._old_name,
                                               old_surname=self._old_surname, new_surname=self._old_surname)
                    self._rename_coop_table(coop_table_suffix + old, coop_table_suffix + new)
                    self._rename_client_table(client_table_suffix + old, client_table_suffix + new)
            except AssertionError as ex:
                app_log.error(f"{repr(self)}: {ex}")

    def _func_name_name(self, items: Dict):
        if self._func_name is not None:
            try:
                if self._func_name == self._c_update_name:
                    assert items.get(self._c_cid) is not None, "cid is missing"
                    assert items.get(self._c_old_name) is not None, "old name is missing"
                    assert items.get(self._c_new_name) is not None, "new name is missing"
                    self._old_name = items.get(self._c_old_name)
                    self._new_name = items.get(self._c_new_name)
                    assert self._old_name != self._new_name, "names can not be equal"
                    self._old_id = items.get(self._c_cid)
                    self._old_surname = items.get(self._c_surname)
                    old, new = self._get_names(old_cid=self._old_id, new_cid=self._old_id,
                                               old_name=self._old_name, new_name=self._new_name,
                                               old_surname=self._old_surname, new_surname=self._old_surname)
                    self._rename_coop_table(coop_table_suffix + old, coop_table_suffix + new)
                    self._rename_client_table(client_table_suffix + old, client_table_suffix + new)
            except AssertionError as ex:
                app_log.error(f"{repr(self)}: {ex}")

    def _func_name_surname(self, items: Dict):
        if self._func_name is not None:
            try:
                if self._func_name == self._c_update_surname:
                    assert items.get(self._c_cid) is not None, "cid is missing"
                    assert items.get(self._c_old_surname) is not None, "old surname is missing"
                    assert items.get(self._c_new_surname) is not None, "new surname is missing"
                    self._old_surname = items.get(self._c_old_surname)
                    self._new_surname = items.get(self._c_new_surname)
                    assert self._old_surname != self._new_surname, "surnames can not be equal"
                    self._old_id = items.get(self._c_cid)
                    self._old_name = items.get(self._c_name)
                    old, new = self._get_names(old_cid=self._old_id, new_cid=self._old_id,
                                               old_name=self._old_name, new_name=self._old_name,
                                               old_surname=self._old_surname, new_surname=self._new_surname)
                    self._rename_coop_table(coop_table_suffix + old, coop_table_suffix + new)
                    self._rename_client_table(client_table_suffix + old, client_table_suffix + new)
            except AssertionError as ex:
                app_log.error(f"{repr(self)}: {ex}")


if __name__ == "__main__":
    UpdateTableNames(func_name="update_id",
                     old_cid=3,
                     new_cid=2,
                     name="ma",
                     surname="sa")
    UpdateTableNames(func_name="update_name",
                     cid=2,
                     old_name="ma",
                     new_name="mb",
                     surname="sa")
    UpdateTableNames(func_name="update_surname",
                     cid=2,
                     old_surname="sa",
                     new_surname="sb",
                     name="mb")
