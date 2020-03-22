import unittest
from hubdbapi.table_functions import (
    publish_table,
    get_table_id,
    delete_table,
    create_and_publish_table,
    get_table_details,
    add_row_to_table,
    get_row_from_table,
    get_table_column_name_to_id_map,
get_all_rows_from_table
)
from tests.config import (
    hs_portalid,
    hs_key
)

class TestFkSelectAndMulti(unittest.TestCase):

    def setUp(self):

        # import json
        # employee_table_id = get_table_id("employee", hs_key)
        # print(json.dumps(get_all_rows_from_table(employee_table_id, hs_portalid), indent=2))
        # self.assertEquals(True, False)

        # employment_status table definition
        employment_status_table_name = "employment_status"
        employment_status_table_definition = {
            "label": "employment status",
            "name": employment_status_table_name,
            "columns": [
                {
                    "name": "status",
                    "type": "TEXT"
                }
            ]
        }
        # Create the employment_status table
        employment_status_table_id = get_table_id(employment_status_table_name, hs_key)
        if employment_status_table_id is not None:
            delete_table(employment_status_table_id, hs_key)
        resp = create_and_publish_table(employment_status_table_definition, hs_key)
        self.assertEqual(employment_status_table_name, resp.get("name"))
        employment_status_table_id = resp.get("id")
        employment_status_col_map = get_table_column_name_to_id_map(employment_status_table_id, hs_portalid)
        employment_status_column_id = employment_status_col_map.get("status")
        add_row_to_table({"values": {str(employment_status_column_id): "1099"}},
                         employment_status_table_id, hs_key)
        add_row_to_table({"values": {str(employment_status_column_id): "W2"}},
                         employment_status_table_id, hs_key)
        publish_table(employment_status_table_id, hs_key)
        employment_status_rows = get_all_rows_from_table(employment_status_table_id, hs_portalid)
        self.employment_status_id_map = {}
        for row in employment_status_rows:
            row_id = row["id"]
            status = row["values"][str(employment_status_column_id)]
            self.employment_status_id_map[status] = row_id
        # employee table definition
        employee_table_name = "employee"
        employee_table_definition = {
            "label": "employee",
            "name": employee_table_name,
            "columns": [
                {
                    "name": "Name",
                    "type": "TEXT"
                },
                {
                    "name": "employment_status",
                    "foreignTableId": employment_status_table_id,
                    "foreignColumnId": employment_status_column_id,
                    "type": "FOREIGN_ID"
                }
            ]
        }
        # Create the employee table
        employee_table_id = get_table_id(employee_table_name, hs_key)
        if employee_table_id is not None:
            delete_table(employee_table_id, hs_key)
        resp = create_and_publish_table(employee_table_definition, hs_key)
        self.assertEqual(employee_table_name, resp.get("name"))
        self.employee_table_id = resp.get("id")
        self.employee_table_col_map = get_table_column_name_to_id_map(employee_table_id, hs_portalid)
        self.name_column_id = self.employee_table_col_map.get("Name")
        self.employment_status_column_id = self.employee_table_col_map.get("employment_status")
        # add_row_to_table()

    def test_add_fk_select_row(self):
        employee_row = {
            "values": {
                str(self.employee_table_col_map['Name']): "Fred Flinstone",
                str(self.employee_table_col_map['employment_status']): [
                    {
                        "id": self.employment_status_id_map["1099"],
                        "type": "foreignid"
                    }
                ]
            }
        }
        employee_row_id = add_row_to_table(employee_row, self.employee_table_id, hs_key).get("id")
        self.assertIsNotNone(employee_row_id)
        publish_table(self.employee_table_id, hs_key)
        newly_added_row = get_row_from_table(employee_row_id, self.employee_table_id, hs_portalid)
        self.assertIsNotNone(newly_added_row)
        self.assertEqual("Fred Flinstone", newly_added_row.get("values").get(str(self.name_column_id)))
        print(newly_added_row.get("values").get(str(self.employment_status_column_id)))


if __name__ == '__main__':
    unittest.main()
