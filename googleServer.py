from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1-_VbefW_BRP1RWYhXhdWdJCj1F4JxsRMwsqQ6yjEtZ8'
RFID_RANGE_NAME = 'Sheet1!A:D'

def main(id):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=RFID_RANGE_NAME).execute()
    values = result.get('values', [])
    condensedValues = []
    if not values:
        print('No data found.')
    else:
        for RFID in values:
            condensedValues += RFID
            print(condensedValues)
        for RFID in values:
            print((RFID[0]))
            print((str(id)))
            if RFID[0] == str(id):
                print("Found em!")

        # targetRow = ord(values.index(eval(str(id)))) - 38
        # STUDENT_NAME_RANGE = 'Sheet1!B' + str(targetRow) + ':D' + str(targetRow)
        # print(STUDENT_NAME_RANGE)


if __name__ == '__main__':
    print(main(1637812764))