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

### Access data
You have two ways of accessing the data on tableau. Both have their advantages and disadvantages.
If you need a quick start, you best use the REST method, where you only have to provide the username and passwort in the secrets file.
If you want to use the existing python library (https://pypi.org/project/tableau-api-lib/), you can go with the methods in the get_lib_data.py file. 

#### With REST-API
##### Set username and password
As a first step, you need to set the username and password as described in the section above. 
If you don't do this, you will be prompted through the command line.

##### Get data
In the main.py file, you have to make sure the get_data_with_rest() method isn't commented out.
As soon as you start the main method, the REST-API example loops through the available workbooks and views available in the config.py file
and stores them in a file named after the view. You can comment out the views you don't need in the config.py file.

##### Filter by date
In the example code, the data is also bing filtered for a single day. You might want to adapt this section 
of the code as you need it.

##### Additional information
You can alter the script according the documentation here: https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api.htm

The code was adapted from the Tableau source on github: https://github.com/tableau/rest-api-samples

#### With the python library
##### Create token on tableau server
First you need to create an access token on tableau servern. You can do this on the mediapulse tableau server instance here: https://tableau.mediapulse.ch/#/signin
Once logged in, take the follwing steps:
1. navigate to your profile section on https://tableau.mediapulse.ch/#/signin
2. in the upper right corner, click on your personal icon
3. go to account settings
4. scroll to the "personal access token" section
5. create a new token and give it a name
6. copy the token value and the name of the token to your personal secrets file 

##### Get data
By executing the main method in the main.py file, the data of available workbooks are downloaded 
and stored in a file named after the view.

##### Get metadata for workbooks and views
With the method get_workbook_metadata and get_view_metadata you can download a csv and json with the currently available
views and workbooks. The information is being stored in a file locally.  

##### Additional information
If you need to get more information please refer to https://pypi.org/project/tableau-api-lib/

If you have any questions, please contact data@mediapulse.ch.