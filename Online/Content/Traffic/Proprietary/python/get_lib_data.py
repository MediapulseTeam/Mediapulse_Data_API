import json

from tableau_api_lib import TableauServerConnection
from tableau_api_lib.utils.querying import get_views_dataframe, get_view_data_dataframe
from configuration.secrets import credentials
from configuration.config import workbook_config


ENCODING = "iso-8859-1"


def get_data_with_lib(meta: bool):
    conn = TableauServerConnection(credentials, env='tableau_online')
    conn.sign_in()

    get_view_data(conn)

    if meta:
        get_workbook_metadata(conn)
        get_view_metadata(conn)

    conn.sign_out()


def get_view_data(conn: TableauServerConnection):
    for wb in workbook_config:
        for view in wb.views:
            print("downloading data for: " + view.v_name)
            view_data_df = get_view_data_dataframe(conn, view_id=view.v_id)
            view_data_df.to_csv(view.v_name + ".csv", index=False, encoding=ENCODING)


def get_workbook_metadata(conn: TableauServerConnection):
    wb_meta = conn.query_workbooks_for_site().json()
    with open("workbooks.json", "w", encoding=ENCODING) as outfile:
        outfile.write(json.dumps(wb_meta, indent=4))


def get_view_metadata(conn: TableauServerConnection):
    view_meta =  get_views_dataframe(conn=conn)
    view_meta.to_csv("views.csv", index=False, encoding=ENCODING)



