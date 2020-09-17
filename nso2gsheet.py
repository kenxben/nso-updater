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

import requests


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


def fix_drive_url(s):
    if s.startswith("https://drive.google.com/uc?export=download&id="):
        return s
    else:
        if s.startswith("https://drive.google.com"):
            url2 = s.replace("/view?usp=sharing", "").replace("?e=download", "")
            gid = url2.split("/")[-1]
            print(gid)
            url2 = f"https://drive.google.com/uc?export=download&id={gid}"
            return url2
    return s


def get_rawdata(url):

    print("Reading url: ", url)
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17',
        'Connection': 'close'
    }
    # http = urllib3.PoolManager(headers=headers)
    # r = http.request('GET', url, preload_content=False, retries=10)
    r = requests.get(url, headers=headers)
    print(f"Status code: {r.status_code}\nHistory: {r.history}\nURL: {r.url}")

    try:
        # case 1: we know it is an excel file
        if (r.url[-4:] == 'xlsx') or (r.url[-4:] == '.xls'):
            df = pd.read_excel(r.content)

        # case 2: it might be an excel file in a google drive link
        else:
            url2 = fix_drive_url(r.url) # not google it returns the same string
            print(f"fixed url: {url2}\n")
            r2 = requests.get(url2, headers=headers)
            df = pd.read_excel(r2.content)
            print("Success!\n")


    # case 3: else, it might be an html uploaded as an excel file:
    except XLRDError as e:
        print("Couldn't load data with pd.read_excel.", e, "\nTrying with pd.read_html")
        print("first bytes in data: ", r.content[:300], "\n")
        df = pd.read_html(r.content, header=[0])[0]
        print("Success!")

    # r.release_conn()
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
            send_report(f"ERROR: Couldn't read excel file at url {item['url']}\n", e)

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
