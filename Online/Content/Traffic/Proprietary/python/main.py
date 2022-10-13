from get_lib_data import get_data_with_lib
from get_rest_data import get_data_with_rest

if __name__ == "__main__":

    # Reading the data from all available views with the tableau library
    # meta      Download the meta data of all workbooks and views available to you
    # get_data_with_lib(meta=True)

    # Reading the data from all available views with the rest method
    # Adapt this code to get filtered data by date
    get_data_with_rest()
