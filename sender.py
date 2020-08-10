import yaml
import os
from settings import EMAIL_CREDS
import requests


def build_payload(recipients, subject, message):
    items = []
    for r in recipients:
        items.append("".join(['{"email": "', r, '"}']))
    rstring = ", ".join(items)
    rstring = "".join(["[", rstring, "]"])
    payload = f'''{{
  "recipients": {rstring},
  "lists": [],
  "contacts": [],
  "attachments": [],
  "title": "{subject}",
  "html": "{message}",
  "methods": {{ 
    "postmark": false,
    "secureSend": false,
    "encryptContent": false,
    "secureReply": false 
  }}
}}'''

    return payload


def send_email(recipients, subject, message):
    key = os.getenv('TRUSTIFI_KEY')
    secret = os.getenv('TRUSTIFI_SECRET')
    trustifi_url = os.getenv('TRUSTIFI_URL')

    # Override if creds are in yaml file
    if os.path.isfile(EMAIL_CREDS):
        with open(EMAIL_CREDS) as stream:
            creds = yaml.safe_load(stream)
        key = creds['TRUSTIFI_KEY']
        secret = creds['TRUSTIFI_SECRET']
        trustifi_url = creds['TRUSTIFI_URL']

    payload = build_payload(recipients, subject, message)
    headers = {
        'x-trustifi-key': key,
        'x-trustifi-secret': secret,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", trustifi_url, headers=headers, data=payload)
    print(response.text.encode('utf8'))
