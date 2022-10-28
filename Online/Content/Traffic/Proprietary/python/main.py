from datetime import date
from get_rest_data import get_data_with_rest, get_data_with_rest_for_date, get_workbooks, get_views

if __name__ == "__main__":

    # uncomment to get all available workbooks
    # print(get_workbooks())

    # uncomment to get all available views for a workbook
    # print(get_views('[ID of workbook]'))

    # Reading the data from all available views with the rest method
    # Adapt this code to get filtered data by date
    get_data_with_rest()

    get_data_with_rest_for_date(date(year=2022, month=9, day=1))
