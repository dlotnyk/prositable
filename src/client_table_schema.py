from client_table_prototype import ClientTable
client_table_suffix = "client_history_"


def create_client_table(table_name: str):
    a = ClientTable()
    a.set_table_name(table_name)
    return a
