from datetime import date
from get_rest_data import get_data_with_rest, get_data_with_rest_for_date

if __name__ == "__main__":

    # Reading the data from all available views with the rest method
    # Adapt this code to get filtered data by date
    get_data_with_rest()

    get_data_with_rest_for_date(date(year=2022, month=5, day=1))
