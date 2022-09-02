# Mediapulse_Data_API
## Online Content Traffic Data

This API allows to pull data proprietary data from the Mediapulse Tableau server. You can use your username and password, which you use to access the Mediapulse Online Content Traffic Data on the Tableau server https://tableau.mediapulse.ch/

If you want to get more information about how to use the Tableau-API, please refer to the Tableau documentation here:
https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api.htm

### Setup
Once you coloned the repository, you can install all needed packages from the Pipfile.
To do this, you can use Pipenv (https://pypi.org/project/pipenv/)

In addition, you also need to keep your own secrets in the secrets file.
To do this, you need to copy and rename the secrets_template.py file in the configuration folder.
Replace the username and password strints in [] with your information 

### Get the workbooks and views
Once you have the virtual environment set up with all packages, you need to get the ids for the workbooks and views available for you.
You can co this by running the get_data.py script:

```
python get_data.py
```
The script prints the workbooks with the Ids. Copy the ID of workbook you want to access into the respective field in the secrets.py file in the configuration folder.

Rerun the script and you will get the available views with the IDs. Copy the ID of the view you want to access into the secrets.py file as well.

### Get the data
Once you have the correct ID of a view in the secrets.py file, you can again run the script and the data will be loaded and written into a data.csv file.

```
python get_data.py
```

You can alter the script according the documentation here: https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api.htm

The code was adapted from the Tableau source on github: https://github.com/tableau/rest-api-samples

If you have any questions, please contact data@mediapulse.ch.
