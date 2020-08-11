import pandas as pd
import urllib3
from xlrd.biffh import XLRDError
from google.oauth2.service_account import Credentials
import gspread
import settings
from sender import send_email
import sys
import os
import json


def send_report(message, error=None):
    print(message, "ERROR:", error)
    recipients = ["kenxben@gmail.com", "samantaamaguayo@gmail.com"]
    msg = "\n".join(["<body>",
                     message,
                     str(error).replace('"', ''),
                     "</body>"]).replace("\n", "<br>")
    if error:
        send_email(recipients,
                   "ERROR: Actualizacion de base de registros sanitarios",
                   msg)
    else:
        send_email(recipients,
                   "REPORTE: Actualizacion exitosa de base de registros sanitarios",
                   msg)

    sys.exit()


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
        print("first bytes in data: ", r.data[:300])
        df = pd.read_html(r.data, header=[0])[0]
        print("Success!")

    r.release_conn()
    return df


def format_data(raw):
    # rename columns
    raw.rename(columns=settings.COL_RENAMER, inplace=True)
    # sort and select columns
    raw = raw[settings.COLS_SORTED]

    return raw


def add_constant_col(df, colname, value):
    df[colname] = value


def upload_data(data, targetID):
    # set up credentials
    scope = ['https://www.googleapis.com/auth/spreadsheets']

    if os.path.isfile(settings.GSHEET_CREDS):  # for local environment
        credentials = Credentials.from_service_account_file(settings.GSHEET_CREDS, scopes=scope)
    else:  # to use secret stored in environment vars
        gc = json.loads(os.getenv("GSHEET_CREDS"))
        credentials = Credentials.from_service_account_info(gc, scopes=scope)
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

    data = []
    for item in settings.URLS:
        # Extract data
        try:
            raw = get_rawdata(item['url'])
        except Exception as e:
            send_report(f"ERROR: Couldn't read excel file at url {item['url']}", e)

        # Add columns with type label
        add_constant_col(raw, "Tipo de producto", item['label'])

        # Format data
        try:
            df = format_data(raw)
        except Exception as e:
            send_report(f"ERROR: Couldn't format data from url {item['url']}\nColumns: {list(raw.columns)}", e)

        data.append(df)

    data = pd.concat(data, ignore_index=True)
    data.fillna('', inplace=True)
    print("Extracted", data.shape[0], "records.")

    # Upload data to gsheets
    print("Uploading data to gsheets...")
    try:
        upload_data(data, settings.TARGET_ID)
    except Exception as e:
        send_report(f"ERROR: Couldn't upload data to {settings.TARGET_ID}", e)

    send_report(f"Updated data:\nhttps://docs.google.com/spreadsheets/d/{settings.TARGET_ID}\n")
    print("Success!")


if __name__ == "__main__":
    main()
