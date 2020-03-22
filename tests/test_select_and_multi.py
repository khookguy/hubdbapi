import unittest
from hubdbapi.table_functions import (
    publish_table,
    get_table_id,
    delete_table,
    create_and_publish_table,
    get_table_details,
    add_row_to_table,
    get_row_from_table,
    get_table_column_name_to_id_map
)
from tests.config import (
    hs_portalid,
    hs_key,
)

select_table_name = "select_test"
select_table_definition = {
    "label": "select test",
    "name": select_table_name,
    "columns": [
        {
            "name": "Name",
            "type": "TEXT"
        },
        {
            "name": "pickone",
            "type": "SELECT",
            "options": [
                {
                    "name": "one",
                    "type": "option"
                },
                {
                    "name": "two",
                    "type": "option"
                },
                {
                    "name": "three",
                    "type": "option"
                }
            ]
        }
    ]
}
select_row = {
    "Name": "Madonna",
    "pickone":
        {
            "name": "one",
            "type": "option"
        }
}

multiselect_table_name = "multiselect_test"
multiselect_table_definition = {
    "label": "multiselect test",
    "name": multiselect_table_name,
    "columns": [
        {
            "name": "Name",
            "type": "TEXT"
        },
        {
            "name": "choices",
            "type": "MULTISELECT",
            "options": [
                {
                    "name": "one",
                    "type": "option"
                },
                {
                    "name": "two",
                    "type": "option"
                },
                {
                    "name": "three",
                    "type": "option"
                }
            ]
        }
    ]
}
multiselect_row = {
    "Name": "Super Tramp",
    "choices": [
        {
            "name": "one",
            "type": "option"
        },
        {
            "name": "three",
            "type": "option"
        }
    ]
}


class TestSelectAndMulti(unittest.TestCase):
    def test_table_creation(self):
        table_id = get_table_id(multiselect_table_name, hs_key)
        if table_id is not None:
            delete_table(table_id, hs_key)
        resp = create_and_publish_table(multiselect_table_definition, hs_key)
        self.assertEqual(multiselect_table_name, resp.get("name"))
        table_id = get_table_id(multiselect_table_name, hs_key)
        delete_table(table_id, hs_key)
        table_id = get_table_id(multiselect_table_name, hs_key)
        self.assertIsNone(table_id)

    def test_insert_select_row(self):
        table_id = get_table_id(select_table_name, hs_key)
        if table_id is not None:
            delete_table(table_id, hs_key)
        table_id = create_and_publish_table(select_table_definition, hs_key).get("id")
        table_details = get_table_details(table_id, hs_portalid)
        values = {}
        for col in table_details.get("columns"):
            name = col["name"]
            id = col["id"]
            value = select_row[name]
            if col["type"] == "SELECT":
                option_id = col["id"]
                value["id"] = option_id
            values[str(id)] = value
        resp_json = add_row_to_table({"values": values}, table_id, hs_key)
        publish_table(table_id, hs_key)
        self.assertGreater(resp_json["id"], 0, "The inserted row should have a non-zero id in HubDB.")
        row_from_table = get_row_from_table(resp_json["id"], table_id, hs_portalid)
        name_to_id_map = get_table_column_name_to_id_map(table_id, hs_portalid)
        self.assertEqual(select_row["Name"], row_from_table["values"][str(name_to_id_map["Name"])])
        self.assertGreater(row_from_table["values"][str(name_to_id_map["pickone"])]["id"], 0)
        table_id = get_table_id(select_table_name, hs_key)
        delete_table(table_id, hs_key)
        table_id = get_table_id(select_table_name, hs_key)
        self.assertIsNone(table_id)

    def test_insert_multiselect_row(self):
        table_id = get_table_id(multiselect_table_name, hs_key)
        if table_id is not None:
            delete_table(table_id, hs_key)
        table_id = create_and_publish_table(multiselect_table_definition, hs_key).get("id")
        table_details = get_table_details(table_id, hs_portalid)
        values = {}
        for col in table_details.get("columns"):
            name = col["name"]
            id = col["id"]
            value = multiselect_row[name]
            if col["type"] == "MULTISELECT":
                option_name_to_id_map = {}
                # build a map of option names to option ids
                for option in col["options"]:
                    option_name_to_id_map[option["name"]] = option["id"]
                # add the option id to each selection option
                for selected_option in value:
                    selected_option["id"] = option_name_to_id_map[selected_option["name"]]
            values[str(id)] = value
        resp_json = add_row_to_table({"values": values}, table_id, hs_key)
        publish_table(table_id, hs_key)
        self.assertGreater(resp_json["id"], 0, "The inserted row should have a non-zero id in HubDB.")
        row_from_table = get_row_from_table(resp_json["id"], table_id, hs_portalid)
        name_to_id_map = get_table_column_name_to_id_map(table_id, hs_portalid)
        self.assertEqual(multiselect_row["Name"], row_from_table["values"][str(name_to_id_map["Name"])])
        self.assertEqual(len(row_from_table["values"][str(name_to_id_map["choices"])]), 2)
        self.assertEqual(row_from_table["values"][str(name_to_id_map["choices"])][0]["type"], "option")
        table_id = get_table_id(multiselect_table_name, hs_key)
        delete_table(table_id, hs_key)
        table_id = get_table_id(multiselect_table_name, hs_key)
        self.assertIsNone(table_id)


if __name__ == '__main__':
    unittest.main()
