from db_create.mediator import Mediator
from db_create.local_db import LocalDb
from operate_main_table import OperateMainTable
from operate_client_table import OperateClientTable
from operate_coop_table import OperateCoopTable


# move to another
class ConcreteMediator(Mediator):
    def __init__(self, db_comp: LocalDb,
                 main_table_comp: OperateMainTable,
                 cl_table_comp: OperateClientTable,
                 coop_table_comp: OperateCoopTable) -> None:
        self._db_comp = db_comp
        self._main_table_comp = main_table_comp
        self._cl_table_comp = cl_table_comp
        self._coop_table_comp = coop_table_comp
        self._coop_table_comp.mediator = self
        self._db_comp.mediator = self
        self._main_table_comp.mediator = self
        self._cl_table_comp.mediator = self

    def notify(self, sender: object, event: str) -> None:
        if event == "A":
            print("Mediator reacts on A and triggers following operations:")
            self._component2.do_c()
        elif event == "D":
            print("Mediator reacts on D and triggers following operations:")
            self._component1.do_b()
            self._component2.do_c()
