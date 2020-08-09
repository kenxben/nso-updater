import pandas as pd
import urllib3
from xlrd.biffh import XLRDError
from google.oauth2.service_account import Credentials
import gspread
import settings


def report_error(message, error):
    # TODO: handle error sending email
    print(message, error)


def get_rawdata(url):

    print("Reading url: ", url)
    # ua = UserAgent()
    http = urllib3.PoolManager(headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'})
    r = http.request('GET', url, preload_content=False)

    try:
        df = pd.read_excel(r.data)
        print("Success!")
    except XLRDError as e:
        print("Couldn't load data with pd.read_excel.", e, "\nTrying with pd.read_html")
        try:
            print("first bytes in data: ", r.data[:300])
            df = pd.read_html(r.data, header=[0])[0]
            print("Success!")
        except Exception as e:
            report_error("ERROR: Couldn't read excel file.", e)
            df = pd.DataFrame(columns=settings.cols_sorted)

    r.release_conn()
    return df


def format_data(raw):

    try:
        # rename columns
        raw.rename(columns=settings.col_renamer, inplace=True)
        # sort and select columns
        raw = raw[settings.cols_sorted]
    except Exception as e:
        report_error("ERROR: formatting data.", e)
        raw = pd.DataFrame()

    return raw


def upload_data(data, targetID):
    # set up credentials
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = Credentials.from_service_account_file(settings.creds_file, scopes=scope)
    gc = gspread.authorize(credentials)

    # Open google sheets document
    sh = gc.open_by_key(targetID)

    # Select worksheet
    worksheet = sh.get_worksheet(0)

    # Update data to worksheet
    worksheet.clear()
    worksheet.update([data.columns.values.tolist()] + data.values.tolist())
    print(f"Uploaded data to https://docs.google.com/spreadsheets/d/{targetID}")


def main():

    # Extract and join data
    data = []
    for url in settings.urls:
        raw = get_rawdata(url)
        df = format_data(raw)
        data.append(df)
    data = pd.concat(data, ignore_index=True)
    data.fillna('', inplace=True)
    print("Extracted", data.shape[0], "records.")

    # Upload data to gsheets
    print("Uploading data to gsheets...")
    upload_data(data, settings.targetID)


if __name__ == "__main__":
    main()
