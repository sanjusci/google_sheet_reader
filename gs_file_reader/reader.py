
__author__ = "Sanju Sci"
__email__ = "sanju.sci9@gmail.com"
__copyright__ = "Copyright 2019."

import os
import sys
sys.path.insert(0, os.getcwd())
from gs_file_reader import *
SMTP_CONFIG = config.SMTP_CONFIG
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'


# The ID and range of a sample spreadsheet.
# SPREADSHEET_ID = # <Your spreadsheet ID>
# RANGE_NAME = # <Your worksheet name>ss

# Capture our current directory


class GoogleFileReader(object):
    service = None

    def __init__(self):
        if not self.service:
            store = file.Storage('config/token.json')
            creds = store.get()
            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets('config/credentials.json', SCOPES)
                creds = tools.run_flow(flow, store)
            self.service = build('sheets', 'v4', http=creds.authorize(Http()))

    def get_google_sheet(self, spreadsheetid, range):
        """
        Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        # Call the Sheets API
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheetid,
                                    range=range).execute()
        return result

    def read_sheet(self, gsheet):
        """
        Converts Google sheet data to a Pandas DataFrame.
        Note: This script assumes that your data contains a header file on the first row!
        Also note that the Google API returns 'none' from empty cells - in order for the code
        below to work, you'll need to make sure your sheet doesn't contain empty cells,
        or update the code to account for such instances.
        """
        header = gsheet.get('values', [])[0]  # Assumes first line is header!
        values = gsheet.get('values', [])[1:]  # Everything else is data.
        if not values:
            print('No data found.')
        else:
            return header, values
        return None, None


def run(sheet_id, range='Sheet1', to='', cc=''):
    try:
        go_obj = GoogleFileReader()
        sheet = go_obj.get_google_sheet(sheet_id, range)
        header, values = go_obj.read_sheet(sheet)
        body = {
            'template': 'soar_service',
            'name': 'All',
            'header': header,
            'records': values,
            'closure_name': 'Shivani Garg',
            'closure': 'Thanks'
        }
        notify_mgr = NotificationManager
        email_obj = notify_mgr.EMAIL()
        recipients_emails = tuple(map(lambda e: e.strip(), to.split(',')))
        cc_recipients = tuple(map(lambda e: e.strip(), cc.split(','))) if cc else ()
        subject = "SOAR Services Team Status [{}]".format(datetime.now().strftime(" %d %b, %Y"))
        email_params = EmailParameters(to=recipients_emails, cc=cc_recipients, body=body, subject=subject)
        notify_mgr.notify_sync(email_obj, email_params)
    except Exception as e:
        print(e)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=__name__.__doc__)
    parser.add_argument("--sheetid", "-sh", help="show sheet id", required=True)
    parser.add_argument("--range", "-r", help="show range", required=False)
    parser.add_argument("--to_email", "-to", help="show to email", required=True)
    parser.add_argument("--cc_email", "-cc", help="show to cc email", required=False)

    # read arguments from the command line
    args = parser.parse_args()

    # check for --version or -V
    range = 'Sheet1'
    if not args.sheetid or not args.to_email:
        print("Please pass relevant arguments!!")
        sys.exit(1)
    print(args.sheetid, args.range, args.to_email)
    if args.range:
        range = args.range
    run(sheet_id=args.sheetid, range=range, to=args.to_email, cc=args.cc_email)



