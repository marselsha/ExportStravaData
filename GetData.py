###### Install required packages
!pip install stravalib
!pip install gspread_pandas



###### Import libraries
#packages for general use
import pickle
import os
import time
import datetime
from datetime import date
import pandas as pd
import shutil
#packages for strava
from stravalib.client import Client
#packages for Google Drive/Sheets
from google.colab import drive
import gspread
from gspread_pandas import Spread



###### Define variables
# Strava
MY_STRAVA_CLIENT_ID = xxxxx
MY_STRAVA_CLIENT_SECRET = 'xxxxx'
CODE = 'xxxxx'
# Google Sheets
GOOGLE_SHEET_ID = 'xxxxx'
LOCATION_OF_STRAVA_TOKEN_ON_GDRIVE = 'gdrive/MyDrive/Colab Notebooks/strava_access_token.pickle'
LOCATION_OF_GOOGLE_TOKEN_ON_GDRIVE = 'gdrive/MyDrive/Colab Notebooks/google_secret.json'
LOCATION_OF_GOOGLE_TOKEN_LOCAL_DIRECTORY = '/root/.config/gspread_pandas/'
LOCATION_OF_GOOGLE_TOKEN_LOCALLY = '/root/.config/gspread_pandas/google_secret.json'
LOCATION_OF_STRAVA_TOKEN_LOCALLY = '../access_token.pickle'




###### Define functions - Strava Authentication
def generate_intial_access_token():
    access_token = client.exchange_code_for_token(client_id=MY_STRAVA_CLIENT_ID, client_secret=MY_STRAVA_CLIENT_SECRET, code=CODE)
    with open('../access_token.pickle', 'wb') as f:
        pickle.dump(access_token, f)


def copy_access_token_from_gdrive():
    shutil.copy(LOCATION_OF_STRAVA_TOKEN_ON_GDRIVE, LOCATION_OF_STRAVA_TOKEN_LOCALLY)
    print("Successfully finished copying Strava access token to local storage")


def load_access_token_and_refresh():
      #if the access token exists in local storage, proceed
    print("Strava access token exists in local storage")

    with open('../access_token.pickle', 'rb') as f:
        access_token = pickle.load(f)

    print('Latest access token read from file:')
    access_token

    if time.time() > access_token['expires_at']:
        print('Strava token has expired, will refresh')
        refresh_response = client.refresh_access_token(client_id=MY_STRAVA_CLIENT_ID, client_secret=MY_STRAVA_CLIENT_SECRET, refresh_token=access_token['refresh_token'])
        access_token = refresh_response
        with open('../access_token.pickle', 'wb') as f:
            pickle.dump(refresh_response, f)
        print('Refreshed Strava token saved to file.')
        client.access_token = refresh_response['access_token']
        client.refresh_token = refresh_response['refresh_token']
        client.token_expires_at = refresh_response['expires_at']

    else:
        print('Token still valid, expires at {}'
              .format(time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(access_token['expires_at']))))
        client.access_token = access_token['access_token']
        client.refresh_token = access_token['refresh_token']
        client.token_expires_at = access_token['expires_at']


def authenticate_strava():
  if os.path.isfile('../access_token.pickle'):
    load_access_token_and_refresh()

  elif os.path.isfile(LOCATION_OF_STRAVA_TOKEN_ON_GDRIVE):
    #if file does not exist locally, but exists on Gdrive, then copy it to local storage
    print("Strava access token isn't stored locally, but is found on Gdrive. Copying to local storage...")
    copy_access_token_from_gdrive()
    load_access_token_and_refresh()

  else:
    print("Strava access token does not exist; generating...")
    generate_intial_access_token()
    copy_access_token_from_gdrive()
    load_access_token_and_refresh()




###### Define functions - fetching Strava data
def get_best_effort_detail_for_activity(activity_id):
  # Create a list of dictionaries from your list of BestEffort objects

  activity = client.get_activity(activity_id)

  data = [{
            'Activity_id': activity.id,
            'Distance_m': int(best_effort.distance),
            'Elapsed_time_sec': best_effort.elapsed_time,
            'Moving_time_sec': best_effort.moving_time,
            'Name': best_effort.name
          } for best_effort in activity.best_efforts]
  # Convert the list of dictionaries into a pandas DataFrame
  #best_efforts_df = pd.DataFrame(data)
  #print(best_efforts_df)
  return data


def get_activities(activity_limit):
  activity_df = pd.DataFrame()

  data = [{
          'Activity_id': activity.id,
          'Start_datetime': activity.start_date_local,
          'Start_date': datetime.datetime.date(activity.start_date_local),
          'Distance_m': int(activity.distance),
          'Elapsed_time_sec': activity.elapsed_time.seconds,
          'Moving_time_sec': activity.moving_time.seconds,
          'Name': activity.name,
          'Type': activity.type,
          'Elevation_gain_m': int(activity.total_elevation_gain),
          'Gear_id': activity.gear_id,
          'Workout_type': activity.workout_type,
        } for activity in client.get_activities(before = "2050-01-01T00:00:00Z",  limit=activity_limit)]

  # Convert the list of dictionaries into a pandas DataFrame
  activity_df = pd.DataFrame(data)

  #filter it down only to Runs
  activity_df = activity_df[activity_df.Type == "Run"]

  return activity_df

  #to view all available fields in Activity, run this:
  #for activity in client.get_activities(after = "2010-01-01T00:00:00Z",  limit=1):
  #  print(activity)






###### Define functions - writing to Google Sheets / Google Drive
def export_df_to_googlesheets(spreadsheet_id, tab_name, dataframe_name):
  #export dataframe to Google Sheets
  spread = Spread(spreadsheet_id, tab_name)
  spread.df_to_sheet(dataframe_name, index=False, sheet=tab_name, start='A1', replace=True)



def get_refresh_date():
  # Create an empty DataFrame
  df = pd.DataFrame(columns=['DateLastRefreshed'])

  # Get today's date
  today = date.today()

  # Add today's date to the first row
  df.loc[0, 'DateLastRefreshed'] = today

  return df




###### Main function
if __name__ == "__main__":
  # Start StravaLib client
  client = Client()

  # Mount Google Drive
  drive.mount('/content/gdrive')
  os.mkdir(LOCATION_OF_GOOGLE_TOKEN_LOCAL_DIRECTORY)
  shutil.copy(LOCATION_OF_GOOGLE_TOKEN_ON_GDRIVE, LOCATION_OF_GOOGLE_TOKEN_LOCALLY)
  

  # Authenticate to Strava
  authenticate_strava()

  # Get high-level Activity detail for the first N activities, save to a dataframe
  activity_df = get_activities(400)

  # Get detailed Activity data (aka best efforts), save to a dataframe
  best_efforts_df = pd.DataFrame()
  for row in activity_df.itertuples():
    best_efforts_df = best_efforts_df.append(get_best_effort_detail_for_activity(row.Activity_id), ignore_index=True)

  # Get today's date, save to a dataframe
  refresh_date_df = get_refresh_date()

  # Export data to Google Sheets
  export_df_to_googlesheets(GOOGLE_SHEET_ID, 'activities', activity_df)
  export_df_to_googlesheets(GOOGLE_SHEET_ID, 'best efforts', best_efforts_df)
  export_df_to_googlesheets(GOOGLE_SHEET_ID, 'refresh date', refresh_date_df)
