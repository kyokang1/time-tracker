# "Work-Life Balance Keeper"

## 1. Summary

Welcome to `"Work-Life Balance Keeper"` (the WLB Keeper or the Keeper) developed by K-young. The application will evaluate your work-life balance status and warn you if you work too hard. Based on the daily work hours the user input in the program, WLB Keeper will calculate the average working hours and display status message according to the pre-defined setting for 4 levels of status. The Keeper stores data online in `Google Spreadsheet` and interacts with the previous work history on real-time basis. And the program creates the work hour summary chart using `Plotly Online Chart Studio` package to sum up your work history and let you know the monthly and yearly work trend.


## 2. Set-up

### 2-1. Prerequisites

It is recommended to set up a virtual environment to ensure Python runs under the following prerequisites:
  + Anaconda 3.7
  + Python 3.7
  + Pip


### 2-2. Installation

Install pip command to install the packages required to run the program. You can run the following command in command line:
```
pip install -r requirements.txt
```

The required packages are as follows:
```
python-dotenv
Flask
Flask-Uploads    
gunicorn
gspread
oauth2client
pylint
plotly
psutil
pytest
requests
```

### 2-3. Google API

As the Keeper stores data online and interacts with previous data real-time basis using `Google Spreadhsset`, you need to obtain the `Google API credentials` and set up the environment in Google spreadsheet. Steps are as follows:

1. Head to [Google Developer Console](https://console.developers.google.com/cloud-resource-manager) and create a new project (or select the one you have.)
2. Click on your project, then from the project page, search for the "Google Sheets API" and enable it. Also search for the "Google Drive API" and enable it. 
3. From either API page, or from the [API Credentials](https://console.developers.google.com/apis/credentials) page, follow a process to create and download credentials to use the APIs. Fill in the form to find out what kind of credentials:

    + API: "Google Sheets API"
    + Calling From: "Web Server"
    + Accessing: "Application Data"
    + Using Engines: "No"

4. Select “New Credentials > Service Account Key”. Then, a JSON file with the credential data that look like below will be downloaded automatically:
```
{
    "private_key_id": "2cd … ba4",
    "private_key": "-----BEGIN PRIVATE KEY-----\nNrDyLw … jINQh/9\n-----END PRIVATE KEY-----\n",
    "client_email": "473000000000-yoursisdifferent@developer.gserviceaccount.com",
    "client_id": "473 … hd.apps.googleusercontent.com",
    "type": "service_account"
}
```
5. Create the directory named `"auth/"` and store the JSON file downloadedhe name of 
   The credential file name should be `google_api_credentials.json` or you can change in the code.
6. Find the value of `client_email` from the JSON credential file.
7. Go to your spreadsheet and share it with a client_email from the step above. 
   Otherwise you’ll get a SpreadsheetNotFound exception when trying to access this spreadsheet with gspread.

Please refer to `https://gspread.readthedocs.io/en/latest/` for more information on API set up.

> NOTE: The  `"auth/"` is ignored from the version control using `.gitignore` file for security purpose. ".gitignore" prevents the secret credentials from being tracked in version control. 


### 2-4. plotly API

As the program creates summary chart using online chart studio `Plotly`, the user needs API Key to use the API and run the program. Please [obtain an "plotly" API Key](https://plot.ly/settings/api#/) (e.g. "abc123") in the link and refer to [how to set up plotly in Python](https://plot.ly/python/getting-started/) for your information.

After obtaining an API Key, you need to input your `"Plotly Username"` and `"Plotly API Key"` and in the file ".env" to specify your real username and API Key like below:

    plotly_user_name = "userkyoung"
    plotly_api_key = "abc123"

> NOTE: The credential information in ".env" file is ignored from the version control using `.gitignore` file for security purpose. ".gitignore" prevents the ".env" file and its secret credentials from being tracked in version control. 


## 3. Usage

### 3-1. Run the app

For this local client version, Use your text editor or the command-line to run a local web server, then view your app in a browser at http://localhost:5000/:

```sh
# Mac Terminal or Windows Git Bash:
FLASK_APP=app flask run

# Windows Command Prompt:
set FLASK_APP=app
flask run
```

> NOTE: you can quit the server by pressing ctrl+c at any time. If you change a file, you'll likely need to restart the server for the changes to take effect.

### 3-2. Input Page

In the input page, user inputs `Date` and `Work hours`. Input page configures input box of "date" as select box to allow only `MM/DD/YYYY` format to prevent invalid input of date. Work hours can only be input with numbers and the minimum value is set as `0` and the maximum value is set as `24` hours. 

### 3-3. Result Page

Using the input hours, the program demonstrates you `daily average work hours`, `total work hours`, and `Work-Life Balance Status` of the latest month on monthly and yearly basis. You can refer to "Data Processing Logic" for calculation logic.

If you click the `daily average work hours` and `total work hours`, the summary charts containing previous history are open automatically in `plotly` platform. You can scale the chart in the platform and manipulate on your own needs. Please visit the [plotly chart studio demo](https://plot.ly/online-chart-maker/) for more details.


### 3-4. Testing

The program has the function to run automated test to see if the program runs as designed. 

Firstly, you need to nstall pytest if you do not install pytest package in the virtual environment. 
    (Note: This is the first time only. You do not need to run this next time.):

```sh
pip install pytest
```

After the installation, you can run the pytest with the simple script like below:
```sh
pytest
```

The designed tests are as follows:
```sh
test_get_records
-> Test to ensure the function returns the the data from Google spreadsheet. 

test_day_of_week
ttest_dow_week
-> Test to ensure the function identifies days of week and distinguishes weekdays and weekends.

test_list_total
-> Test the function to sum the values in the list.

test_total_hour_ytd
test_avg_hour_ytd
-> Test the key functions to calculate the total and average of hours.
```


## 4. Data Processing Logic

Interacting with previous work data, the program calculates the daily average work hours, which is `total work hours` divided by `number of weekdays`. `Total work hours` is the sum of all the work hours regardless it is weekdays or weekends, and it is divided by `number of weekdays`. So it is true that the work hour increases if you work in weekends so as to aggrevate the evaluation of work-life balance. Status messages are separate for Month-To-Date WLB status and Year-To-Date status.

Based on the daily average work hours, The Keeper will evaluates the Work-Life Blaance Status and displays the status message based on the pre-configured threshold. The four status message and the work hours are as follows:

  1. `SAFE` - If the daily average work hours is 8 hours or less
  2. `WATCH` - If the daily average work hours is more than 8 hours and 9 hours or less
  3. `WARNING` - If the daily average work hours is more than 9 hours and 10 hours or less
  4. `DANGER` - If the daily average work hours exceeds 10 hours

> NOTE: you can change the thershold hours and the status message in the code.

`Year-To-Date Total Work Hour` charts are preconfigured with `benchmark` total work hours of Germany, US, and South Korea using their [2017 OECD Statistics - Hours Worked](https://data.oecd.org/emp/hours-worked.htm). (Germany with 1,356 hours a year is configured with `green` line, US with 1,780 hours is with `yellow` line, and S. Korea with 2,024 hours is configured with `red` line.

> NOTE: you can also change the benchmark in the code.

## 5. [License](LICENSE)


## 6. Thank You Note by K-young

Thank you for using. Hope the tool helps your life balanced with your work! 

We should remember... 
Family is the most important thing in your life! 
Other than that, anything can wait.

