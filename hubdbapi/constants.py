hubdb_get_all_tables_url_template = "https://api.hubapi.com/hubdb/api/v2/tables?hapikey={hs_key}"
hubdb_create_table_url_template = "https://api.hubapi.com/hubdb/api/v2/tables?hapikey={hs_key}"
hubdb_delete_table_url_template = "https://api.hubapi.com/hubdb/api/v2/tables/{table_id}?hapikey={hs_key}"
hubdb_insert_table_row_url_template = "https://api.hubapi.com/hubdb/api/v2/tables/{table_id}/rows/?hapikey={hs_key}"
hubdb_publish_table_url_template = "https://api.hubapi.com/hubdb/api/v2/tables/{table_id}/publish?hapikey={hs_key}"
hubdb_get_table_details_url_template = "https://api.hubapi.com/hubdb/api/v2/tables/{table_id}?portalId={portal_id}"
hubdb_add_row_to_table_url_template = "https://api.hubapi.com/hubdb/api/v2/tables/{table_id}/rows?hapikey={hs_key}"
hubdb_get_all_rows_from_table_url_template = \
    "https://api.hubapi.com/hubdb/api/v2/tables/{table_id}/rows?portalId={portal_id}"
