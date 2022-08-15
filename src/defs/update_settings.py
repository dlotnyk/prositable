from typing import Tuple, Optional, List
from logger import log_settings
app_log = log_settings()


class UpdateSettings:
    _c_update_id = "update_id"
    _c_update_name = "update_name"
    _c_update_surname = "update_surname"
    _c_coop_prefix = "coop"
    _c_client_prefix = "client"
    _separator = "_"
    _change_func_list: Tuple = (_c_update_id, _c_update_name, _c_update_surname)

    def __init__(self,
                 fname: str,
                 args: Tuple,
                 table_list: List):
        try:
            self._old_id: Optional[int] = None
            self._new_id: Optional[int] = None
            self._old_name: Optional[str] = None
            self._new_name: Optional[str] = None
            self._old_surname: Optional[str] = None
            self._new_surname: Optional[str] = None
            assert fname in self._change_func_list, "func not compatible"
            self._fname = fname
            self._args = args
            self._old_id = args[0]
            b: List = list(filter(lambda p: len(p.split("_")) == 5, table_list))
            tables: List = list(filter(lambda ff: int(ff.split("_")[4]) == self._old_id, b))
            self._coop_table: List = list(filter(lambda ct: self._c_coop_prefix in ct, tables))
            self._client_table: List = list(filter(lambda ct: self._c_client_prefix in ct, tables))
            self._parse_coop_table()
            self._get_settings()
        except AssertionError as ex:
            app_log.error(f"{ex}")

    def __repr__(self) -> str:
        return "UpdateSettings"

    @property
    def new_id(self) -> int:
        return self._new_id

    @property
    def old_id(self) -> int:
        return self._old_id

    @property
    def new_name(self) -> str:
        return self._new_name

    @property
    def old_name(self) -> str:
        return self._old_name

    @property
    def new_surname(self) -> str:
        return self._new_surname

    @property
    def old_surname(self) -> str:
        return self._old_surname

    def _parse_coop_table(self) -> None:
        if self._coop_table:
            item = self._coop_table[0]
            parsed = item.split(self._separator)
            self._old_name = parsed[2]
            self._old_surname = parsed[3]

    def _get_id(self) -> None:
        if self._fname == self._c_update_id:
            self._new_id = self._args[1]
            self._new_name = self._old_name
            self._new_surname = self._old_surname

    def _get_name(self) -> None:
        if self._fname == self._c_update_name:
            self._new_id = self._old_id
            self._new_name = self._args[1]
            self._new_surname = self._old_surname

    def _get_surname(self) -> None:
        if self._fname == self._c_update_surname:
            self._new_id = self._old_id
            self._new_name = self._old_name
            self._new_surname = self._args[1]

    def _get_settings(self) -> None:
        if self._coop_table:
            self._get_id()
            self._get_name()
            self._get_surname()
        else:
            self._old_id = None

    def is_settings_ok(self) -> bool:
        return not(self._old_id is None or self._new_id is None or self._old_name is None or self._new_name is None or
                   self._old_surname is None or self._new_surname is None)


if __name__ == "__main__":
    a = ['client_history_Name_Surname_2', 'coop_history_Name_Surname_2', 'main_table']
    b = UpdateSettings("update_surname", (2, "NewName", ), a)
    print(f"new_id: {b.new_id}")
    print(f"old_id: {b.old_id}")
    print(f"new_name: {b.new_name}")
    print(f"old_name: {b.old_name}")
    print(f"new_surname: {b.new_surname}")
    print(f"old_surname: {b.old_surname}")
    print(f"Good: {b.is_settings_ok()}")


