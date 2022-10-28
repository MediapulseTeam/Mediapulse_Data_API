"""
# This script prints out users by Tableau Server group by site
#
# To run the script, you must have installed Python 2.7.9 or later,
# plus the 'requests' library:
#   http://docs.python-requests.org/en/latest/
#
# Run the script in a terminal window by entering:
#   python users_by_group.py <server_address> <username>
#
#   You will be prompted for site id, and group name
#   There is also an option to print out all groups
#   See the main() method for details
#
# This script requires a server administrator or a site administrator.
#
# The file version.py must be in the local folder with the correct API version number
"""

import xml.etree.ElementTree as ET # Contains methods used to build and parse XML
import sys
import getpass
import requests # Contains methods used to make HTTP requests
import pandas as pd
import numpy
from version import VERSION
from datetime import date, timedelta
from typing import List

from configuration.secrets import Config
from configuration.config import workbook_config, START_DATE

# The namespace for the REST API is 'http://tableausoftware.com/api' for Tableau Server 9.0
# or 'http://tableau.com/api' for Tableau Server 9.1 or later
XMLNS = {'t': 'http://tableau.com/api'}

ENCODING = 'utf-8'
CHUNK_DAYS = 30

# If using python version 3.x, 'raw_input()' is changed to 'input()'
if sys.version[0] == '3': raw_input=input

class ApiCallError(Exception):
    """ ApiCallError """
    pass

class UserDefinedFieldError(Exception):
    """ UserDefinedFieldError """
    pass

def _encode_for_display(text):
    """
    Encodes strings so they can display as ASCII in a Windows terminal window.
    This function also encodes strings for processing by xml.etree.ElementTree functions.

    Returns an ASCII-encoded version of the text.
    Unicode characters are converted to ASCII placeholders (for example, "?").
    """
    return text.encode('ascii', errors="backslashreplace").decode(ENCODING)

def _check_status(server_response, success_code):
    """
    Checks the server response for possible errors.

    'server_response'       the response received from the server
    'success_code'          the expected success code for the response
    Throws an ApiCallError exception if the API call fails.
    """
    if server_response.status_code != success_code:
        parsed_response = ET.fromstring(server_response.text)

        # Obtain the 3 xml tags from the response: error, summary, and detail tags
        error_element = parsed_response.find('t:error', namespaces=XMLNS)
        summary_element = parsed_response.find('.//t:summary', namespaces=XMLNS)
        detail_element = parsed_response.find('.//t:detail', namespaces=XMLNS)

        # Retrieve the error code, summary, and detail if the response contains them
        code = error_element.get('code', 'unknown') if error_element is not None else 'unknown code'
        summary = summary_element.text if summary_element is not None else 'unknown summary'
        detail = detail_element.text if detail_element is not None else 'unknown detail'
        error_message = '{0}: {1} - {2}'.format(code, summary, detail)
        raise ApiCallError(error_message)
    return

def sign_in(server, username, password, site):
    """
    Signs in to the server specified with the given credentials

    'server'   specified server address
    'username' is the name (not ID) of the user to sign in as.
               Note that most of the functions in this example require that the user
               have server administrator permissions.
    'password' is the password for the user.
    'site'     is the ID (as a string) of the site on the server to sign in to. The
               default is "", which signs in to the default site.
    Returns the authentication token and the site ID.
    """
    url = server + "/api/{0}/auth/signin".format(VERSION)

    # Builds the request
    xml_request = ET.Element('tsRequest')
    credentials_element = ET.SubElement(xml_request, 'credentials', name=username, password=password)
    ET.SubElement(credentials_element, 'site', contentUrl=site)
    xml_request = ET.tostring(xml_request)

    # Make the request to server
    server_response = requests.post(url, data=xml_request)
    _check_status(server_response, 200)

    # ASCII encode server response to enable displaying to console
    server_response = _encode_for_display(server_response.text)

    # Reads and parses the response
    parsed_response = ET.fromstring(server_response)

    # Gets the auth token and site ID
    token = parsed_response.find('t:credentials', namespaces=XMLNS).get('token')
    site_id = parsed_response.find('.//t:site', namespaces=XMLNS).get('id')
    # user_id = parsed_response.find('.//t:user', namespaces=XMLNS).get('id')
    return token, site_id

def sign_out(server, auth_token):
    """
    Destroys the active session and invalidates authentication token.

    'server'        specified server address
    'auth_token'    authentication token that grants user access to API calls
    """
    url = server + "/api/{0}/auth/signout".format(VERSION)
    server_response = requests.post(url, headers={'x-tableau-auth': auth_token})
    _check_status(server_response, 204)
    return


def setup_connection():
    server = Config.server
    username = Config.username
    password = Config.password
    site_id = Config.site_id
    if len(sys.argv) > 1:
        server = sys.argv[1]
        username = sys.argv[2]
    # Prompt for a username
    if username == "":
        username = raw_input("\nUser name: ")
    # Prompt for password
    if password == "":
        password = getpass.getpass("Password: ")
    print("\nSigning in to obtain authentication token")
    auth_token, site_id = sign_in(server, username, password, site_id)
    return auth_token, server, site_id


def get_workbooks():
    """
    Returns the workbooks for the site
    """
    auth_token, server, site_id = setup_connection()
    url = server + "/api/{0}/sites/{1}/workbooks".format(VERSION, site_id)
    server_response = requests.get(url, headers={'x-tableau-auth': auth_token})
    _check_status(server_response, 200)
    xml_response = ET.fromstring(_encode_for_display(server_response.text))
    workbooks = xml_response.findall('.//t:workbook', namespaces=XMLNS)
    all = []
    for workbook in workbooks:
        all.append([workbook.get('name'),workbook.get('id')])
    return all


def get_views(workbook_id):
    """
    Returns the views for a workbook
    """
    auth_token, server, site_id = setup_connection()
    url = server + "/api/{0}/sites/{1}/workbooks/{2}/views".format(VERSION, site_id, workbook_id)
    server_response = requests.get(url, headers={'x-tableau-auth': auth_token})
    _check_status(server_response, 200)
    xml_response = ET.fromstring(_encode_for_display(server_response.text))
    views = xml_response.findall('.//t:view', namespaces=XMLNS)
    all = []
    for view in views:
        all.append([view.get('name'),view.get('id')])
    return all


def get_data(server, auth_token, site_id, view_id, chunked):
    """
    Returns the data for a view in a string
    """
    url = server + "/api/{0}/sites/{1}/views/{2}/data".format(VERSION, site_id, view_id)
    if chunked:
        out = get_chunked_data(auth_token, url)
    else:
        out = get_unchunked_data(auth_token, url)
    return out


def get_unchunked_data(auth_token, url):
    server_response = requests.get(url, headers={'x-tableau-auth': auth_token})
    server_response.encoding = ENCODING
    _check_status(server_response, 200)
    out = server_response.text
    return out


def get_chunked_data(auth_token, url):
    data_list = _get_date_list(start_year=START_DATE.year, start_month=START_DATE.month, start_day=START_DATE.day)
    nb_of_chunks = round((date.today() - START_DATE).days / CHUNK_DAYS)
    data_chunks = numpy.array_split(data_list, nb_of_chunks)
    out = ""
    print(f"number of chunks: {len(data_chunks)}")
    num = 0
    for chunk in data_chunks:
        chunk_string = ','.join([str(item) for item in chunk])
        chunk_url = url + f'?vf_Date={chunk_string}'
        server_response = requests.get(chunk_url, headers={'x-tableau-auth': auth_token})
        server_response.encoding = ENCODING
        _check_status(server_response, 200)
        out += server_response.text
        num += 1
        print(f'chunk number: {num}')
    return out


def _get_date_list(start_year: int, start_month: int, start_day: int) -> List:
    end_date = date.today()
    start_date = date(year=start_year, month=start_month, day=start_day)
    all_dates = []
    for n in range(int((end_date - start_date).days) + 1):
        all_dates.append((start_date + timedelta(n)).strftime("%Y-%m-%d"))
    return all_dates


def get_data_for_date(server, auth_token, site_id, view_id, year: int, month: int, day: int):
    """
    Returns the data for a view
    """
    url = server + "/api/{0}/sites/{1}/views/{2}/data".format(VERSION, site_id, view_id)
    url = url + f'?vf_Date={year}-{month}-{day}'
    server_response = requests.get(url, headers={'x-tableau-auth': auth_token})
    server_response.encoding = ENCODING
    _check_status(server_response, 200)
    return server_response.text


def trim_newline(data):
    data = data.replace('\n', '')
    return data


def remove_header_lines(data_df: pd.DataFrame) -> pd.DataFrame:
    print(f"Dataframe before dropping empty rows: {data_df.shape[0]}")
    data_df = data_df[data_df[0] != '']
    print(f"Dataframe after dropping empty rows: {data_df.shape[0]}")
    return data_df


def format_numbers(data: pd.DataFrame, col: str):
    data[col].replace(',', '', inplace=True, regex=True)
    return data


def post_process(data: str) -> pd.DataFrame:
    data = trim_newline(data)
    data= data.rstrip("\r") # remove last empty line
    if data == '': return None
    data_df = pd.DataFrame([x.split(';') for x in data.split('\r')])
    data_df = remove_header_lines(data_df)
    data_df = data_df.rename(columns=data_df.iloc[0]).drop(data_df.index[0])
    # Depending on the view you are accessing, you might need to adapt the following lines
    if 'Measure Values' in data_df:
        data_df = format_numbers(data_df, 'Measure Values')
    return data_df


def get_data_with_rest():
    auth_token, server, site_id = setup_connection()
    print("-------------------- data -------------------")
    for wb in workbook_config:
        for view in wb.views:
            print(f'getting data for view: {view.v_name}')
            data_df = post_process(get_data(server, auth_token, site_id, view.v_id, view.date_chunks))
            # Do whatever you want with the data you receive in the following section
            if not data_df is None:
                data_df.to_csv(view.v_name+".csv", index=False, encoding=ENCODING)

    print("\nSigning out and invalidating the authentication token")
    sign_out(server, auth_token)


def get_data_with_rest_for_date(date: date):
    auth_token, server, site_id = setup_connection()
    print("-------------------- data filtered by day-------------------")
    # This section filters the data for a specific day. Adapt according to your needs.
    for wb in workbook_config:
        for view in wb.views:
            if view.date_chunks:
                data_df = post_process(get_data_for_date(server, auth_token, site_id, view.v_id,
                                             year=date.year, month=date.month, day=date.day))
                '''
                Do whatever you want with the data you recive in the following section
                '''
                if not data_df is None:
                    data_df.to_csv(view.v_name+"_"+date.strftime('%y%m%d')+".csv", index=False, encoding=ENCODING)

    print("\nSigning out and invalidating the authentication token")
    sign_out(server, auth_token)
