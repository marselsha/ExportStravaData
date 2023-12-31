# ExportStravaData
This code does the following:
1. Connect to Strava API using StravaLib to export Activity and Activity Best Effort data
2. Load the data into Google Sheets

After the data is loaded into Google Sheets, I visualize and analyze it using Tableau. The resulting workbook is published on my Tableau Public profile: https://public.tableau.com/app/profile/marsel.shamgunov

# Helpful resources used to write this code: 
https://stravalib.readthedocs.io/en/latest/get-started/activities.html

https://medium.com/analytics-vidhya/accessing-user-data-via-the-strava-api-using-stravalib-d5bee7fdde17

# Things you need to do before running this code

## Connect to your Google Sheets:

Basic steps:
1. Enable Google Sheets API on your Google Account that will have this Google Sheet
2. Create a Service Account
3. Export Service Account's json credential file
4. Grant edit access to the Google Sheet to your Service Account's email address
5. Replace variables in code to properly ingest the json credential file

Detailed guide: https://medium.com/mlearning-ai/how-to-access-google-sheets-on-google-colaboratory-8766b3a0996f

## Generating the initial CODE variable: 

Basic steps:
1. Create your Strava API application
2. Get your Client ID
3. Replace the Client ID in this URL, and open the URL:
http://www.strava.com/oauth/authorize?client_id=108997&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=profile:read_all,activity:read_all
4. Using the URL above, approve the access request and hit OK
5. Copy the CODE value from the resulting URL

Detailed guide: https://medium.com/analytics-vidhya/accessing-user-data-via-the-strava-api-using-stravalib-d5bee7fdde17
 

## Update all variables in the code
