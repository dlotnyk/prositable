class MainTableColumns:
    c_client_id = "client_id"
    c_name = "name"
    c_surname = "surname"
    c_known_from = "known_from"
    c_rc = "rc"
    c_first_contact = "first_contact"
    c_phone = "phone"
    c_address = "address"
    c_education = "education"
    c_email = "email"
    c_birth = "birth"
    c_age = "age"
    c_work_type = "work_type"
    c_family_status = "family_status"
    c_title = "title"
    c_city = "city"
    c_children = "children"
    c_income = "income"
    c_income2 = "income2"
    c_test = "test"


class AuxTableColumns:
    c_entry_id = "entry_id"
    c_date = "date"
    c_tasks = "tasks"
    c_notes = "notes"


class ClientTableColumns(AuxTableColumns):
    c_client_type = "client_type"


class CoopTableColumns(AuxTableColumns):
    c_coop_type = "coop_type"


if __name__ == "__main__":
    print(MainTableColumns.c_client_id)
    print(ClientTableColumns.c_entry_id)

