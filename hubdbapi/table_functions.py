import requests
import json
from hubdbapi.constants import (
    hubdb_publish_table_url_template,
    hubdb_get_all_tables_url_template,
    hubdb_delete_table_url_template,
    hubdb_create_table_url_template,
    hubdb_get_table_details_url_template,
    hubdb_add_row_to_table_url_template,
    hubdb_get_all_rows_from_table_url_template
)


def get_table_column_name_to_id_map(table_id, portal_id):
    table_details = get_table_details(table_id, portal_id)
    name_to_id_map = {}
    for col in table_details.get("columns"):
        name = col["name"]
        col_id = col["id"]
        name_to_id_map[name] = col_id
    return name_to_id_map


def get_row_from_table(row_id, table_id, portal_id):
    hubdb_get_all_rows_from_table_url = hubdb_get_all_rows_from_table_url_template.format(
        **{'table_id': table_id, 'portal_id': portal_id})
    url_params = {'hs_id__eq': row_id}
    resp = requests.get(hubdb_get_all_rows_from_table_url, params=url_params, headers={})
    resp.raise_for_status()
    row_array = resp.json().get("objects")
    if row_array is None or len(row_array) == 0:
        return None
    return row_array[0]


def add_row_to_table(row, table_id, hs_key):
    hubdb_add_row_to_table_url = hubdb_add_row_to_table_url_template.format(**{'table_id': table_id, 'hs_key': hs_key})
    resp = requests.post(hubdb_add_row_to_table_url,
                         headers={"content-type": "application/json"},
                         data=json.dumps(row))
    resp.raise_for_status()
    return resp.json()


def create_table(table_definition, hs_key):
    hubdb_create_table_url = hubdb_create_table_url_template.format(**{'hs_key': hs_key})
    resp = requests.post(hubdb_create_table_url,
                         headers={"content-type": "application/json"},
                         data=json.dumps(table_definition))
    resp.raise_for_status()
    return resp.json()


def create_and_publish_table(table_definition, hs_key):
    return publish_table(create_table(table_definition, hs_key)["id"], hs_key)


def get_table_id(table_name, hs_key):
    all_tables = get_all_tables(hs_key)
    if all_tables.get("objects") is None:
        return None
    table_id = None
    for table in all_tables["objects"]:
        if table_name == table.get("name"):
            table_id = table.get("id")
            break
    return table_id


def delete_table(table_id, hs_key):
    hubdb_delete_table_url = hubdb_delete_table_url_template.format(
        **{'table_id': table_id, 'hs_key': hs_key})
    resp = requests.delete(hubdb_delete_table_url, headers={})
    resp.raise_for_status()


def get_table_details(table_id, portal_id):
    hubdb_get_table_details_url = hubdb_get_table_details_url_template.format(
        **{'table_id': table_id, 'portal_id': portal_id})
    resp = requests.get(hubdb_get_table_details_url, headers={})
    resp.raise_for_status()
    return resp.json()


def get_all_tables(hs_key):
    hubdb_get_all_tables_url = hubdb_get_all_tables_url_template.format(**{'hs_key': hs_key})
    resp = requests.get(hubdb_get_all_tables_url, headers={})
    resp.raise_for_status()
    return resp.json()


def publish_table(table_id, hs_key):
    hubdb_publish_table_url = hubdb_publish_table_url_template.format(
        **{'table_id': table_id, 'hs_key': hs_key})
    resp = requests.put(hubdb_publish_table_url, headers={"content-type": "application/json"},
                        data=json.dumps({'value': 0}))
    resp.raise_for_status()
    return resp.json()
