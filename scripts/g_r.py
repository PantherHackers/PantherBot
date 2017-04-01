
#gr time random 2/1/18 5/1/18
import datetime
import pandas
from collections import Counter
from sqlalchemy import create_engine
engine = create_engine('mysql://root@localhost:3306/pantherbot_test', echo=False)

def generate_report(response, args):
    if args[0] == 'time':
        if len(args)<4:
            return ["ERROR: Please use the following syntax `time random 2/1/18 5/1/18`"]
        return time(args[2::], args[1])

    if args[0] == 'top_users':
        pass

    if args[0] == 'emoji':
        pass

    if args[0] == 'channel':
        pass

def time(range, channel='all'):
    try:
        v = [datetime.datetime.strptime(x, "%m/%d/%y").date() for x in range]
    except ValueError:
        return ["Please input time in the syntax of mm/dd/yy"]
    q = None
    if channel == 'all':
        q = engine.execute("SELECT hour FROM channelActivity WHERE day_of_month >= %s and day_of_month <= %s and month >= %s and month <= %s and year >= %s and year <= %s", v[0].day, v[1].day, v[0].month, v[1].month, v[0].year, v[1].year).fetchall()
    else:
        q = engine.execute("SELECT hour FROM channelActivity WHERE channel_id = (SELECT slack_id FROM channels WHERE name = %s) and day_of_month >= %s and day_of_month <= %s and month >= %s and month <= %s and year >= %s and year <= %s", channel, v[0].day, v[1].day, v[0].month, v[1].month, v[0].year, v[1].year).fetchall()

    cnt = Counter()
    for v in q:
        cnt[v[0]] += 1

    i = 1
    hour=count=[]
    while i <= 24:
        hour.append(i)
        count.append(cnt[i])
        i += 1

    df = pandas.DataFrame({'Count':count}, index=hour)
    df.columns.name = 'Hour'
    return [str(df)]
    


    # report = """ 

    # +--------+--------+
    # |__hour__|__count_|
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # |   {}   |   {}   |  
    # +--------+--------+

    # """



# from __future__ import print_function
# import httplib2
# import os

# from apiclient import discovery
# from oauth2client import client
# from oauth2client import tools
# from oauth2client.file import Storage

# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None

# # If modifying these scopes, delete your previously saved credentials
# # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
# SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
# CLIENT_SECRET_FILE = 'secrets/client_secret.json'
# APPLICATION_NAME = 'PantherBot'


# def get_credentials():
#     """Gets valid user credentials from storage.

#     If nothing has been stored, or if the stored credentials are invalid,
#     the OAuth2 flow is completed to obtain the new credentials.

#     Returns:
#         Credentials, the obtained credential.
#     """
#     home_dir = os.path.expanduser('~')
#     credential_dir = os.path.join(home_dir, '.credentials')
#     if not os.path.exists(credential_dir):
#         os.makedirs(credential_dir)
#     credential_path = os.path.join(credential_dir,
#                                    'sheets.googleapis.com-python-quickstart.json')

#     store = Storage(credential_path)
#     credentials = store.get()
#     if not credentials or credentials.invalid:
#         flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
#         flow.user_agent = APPLICATION_NAME
#         if flags:
#             credentials = tools.run_flow(flow, store, flags)
#         else: # Needed only for compatibility with Python 2.6
#             credentials = tools.run(flow, store)
#         print('Storing credentials to ' + credential_path)
#     return credentials

# def main():
#     """Shows basic usage of the Sheets API.

#     Creates a Sheets API service object and prints the names and majors of
#     students in a sample spreadsheet:
#     https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
#     """
#     credentials = get_credentials()
#     http = credentials.authorize(httplib2.Http())
#     discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
#                     'version=v4')
#     service = discovery.build('sheets', 'v4', http=http,
#                               discoveryServiceUrl=discoveryUrl)

#     spreadsheetId = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
#     rangeName = 'Class Data!A2:E'
#     result = service.spreadsheets().values().get(
#         spreadsheetId=spreadsheetId, range=rangeName).execute()
#     values = result.get('values', [])

#     if not values:
#         print('No data found.')
#     else:
#         print('Name, Major:')
#         for row in values:
#             # Print columns A and E, which correspond to indices 0 and 4.
#             print('%s, %s' % (row[0], row[4])