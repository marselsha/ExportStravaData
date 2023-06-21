# ExportStravaData
Use Python to connect to Strava API and retrieve data on my tracked runs. This data is then exported to Google Sheets and visualized in Tableau Public. 

# Helpful resources used to write this code: 
https://stravalib.readthedocs.io/en/latest/get-started/activities.html
https://medium.com/analytics-vidhya/accessing-user-data-via-the-strava-api-using-stravalib-d5bee7fdde17

# Generating the initial CODE variable: 
1. Create your Strava API application
2. Get your Client ID
3. Replace the Client ID in this URL, and open the URL:
#http://www.strava.com/oauth/authorize?client_id=108997&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=profile:read_all,activity:read_all
4. Using the URL above, approve the access request and hit OK
5. Copy the CODE value from the resulting URL 
