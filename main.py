from __future__ import print_function

# Steam Stuff

from steam import Steam
from decouple import config

KEY = config("STEAM_API_KEY")

steam = Steam(KEY)

# arguments: steamid
STEAMID = config("STEAM_ID")
user = steam.users.get_owned_games(STEAMID)
gameList = user["games"]
gameNames = []

for game in gameList:
    gameNames.append([game["name"]])
gameNames = sorted(gameNames)
print(gameNames)


# Google Stuff

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google.auth

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = config("SPREADSHEET_ID")
RANGE_NAME = 'A:A'

creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
try:
    service = build('sheets', 'v4', credentials=creds)
    request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME, valueInputOption="USER_ENTERED", body={"values": gameNames})
    response = request.execute()
    print(response)

except HttpError as error:
    print(f"An error occurred: {error}")

