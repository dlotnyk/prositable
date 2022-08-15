from typing import Tuple, Optional, Dict, List


class UpdateSettings:
    _c_update_id = "update_id"
    _c_update_name = "update_name"
    _c_update_surname = "update_surname"
    _separator = "_"
    _change_func_list: Tuple = (_c_update_id, _c_update_name, _c_update_surname)

    def __init__(self,
                 fname: str,
                 args: Tuple,
                 table_list: List):
        self._fname = fname
        self._args = args
        self._old_id = args[0]
        self._tables = filter(lambda p: int(p.split(self._separator)[4]) != self._old_id, table_list)

        print(self._old_id)
        print(args)
        print(list(self._tables))
        self._new_id: Optional[int] = None
        self._old_name: Optional[str] = None
        self._new_name: Optional[str] = None
        self._old_surname: Optional[str] = None
        self._new_surname: Optional[str] = None

    def _get_id(self):
        if self._fname == self._c_update_id:
            pass

    def get_settings(self) -> Dict:
        resp: Dict = dict()
        if self._fname in self._change_func_list:
            if self._fname == self._c_update_id:
                pass
        return resp


if __name__ == "__main__":
    a = ['client_history_Name_Surname_2', 'coop_history_Name_Surname_2', 'main_table']
    # UpdateSettings("some", (2,), a)
    c = a[0].split("_")[3]
    print(c)
    try:
        b = list(filter(lambda p: len(p.split("_")) == 5, a))
        c = filter(lambda ff: ff.split("_")[4] == "2", b)
        print(list(c))
    except IndexError:
        print("not work")

