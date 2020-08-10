import smtplib, ssl
import yaml
import os
from email.message import EmailMessage
from settings import EMAIL_CREDS


def send_email(recipient, subject, message):

    username = os.getenv('USER_NAME')
    password = os.getenv('PASSWORD')
    email = os.getenv('EMAIL')
    servername = os.getenv('SERVER')
    port = os.getenv('PORT')

    if os.path.isfile(EMAIL_CREDS):
        with open(EMAIL_CREDS) as stream:
            creds = yaml.safe_load(stream)
        username = creds['USER_NAME']
        password = creds['PASSWORD']
        email = creds['EMAIL']
        servername = creds['SERVER']
        port = creds['PORT']

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = recipient

    context = ssl.create_default_context()

    try:
        s = smtplib.SMTP(servername, port)
        s.ehlo()
        s.starttls(context=context)
        s.ehlo()
        s.login(username, password)
        s.send_message(msg)
        s.quit()
        print('Email sent.')
    except Exception as e:
        print('Can\'t send the Email.', e)
