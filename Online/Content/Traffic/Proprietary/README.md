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
Replace the username and password strings in [] with your personal credentials. 

### Get the data
The script loops through the list of available views. They are listed in the config.py file. All these views are 
optimized access with the API.

You can access the data by executing the main.py file

```
python main.py
```
With the initial setting, the script downloads all data for all available views (this takes a while). 
The process is being chunked, as the API woul time out otherwise.
If you still get time out messages, you can reduce the amount of days being downloaded 
at once (CHUNK_DAYS in the get_rest_data.py file).

The initial setup also demonstrates how to get data for a single day. You might need this to update your local
data in the future.

You can alter the script according the documentation here: https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api.htm

The code was adapted from the Tableau source on github: https://github.com/tableau/rest-api-samples


If you have any questions, please contact data@mediapulse.ch.