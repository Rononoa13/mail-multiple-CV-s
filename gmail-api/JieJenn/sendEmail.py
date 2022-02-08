from getting_started import get_service

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import base64

from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fileinput import filename
import mimetypes

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']

if __name__ == '__main__':

    service = get_service()

    email_msg = 'You won 100,000$'
    message = MIMEMultipart()
    message['to'] = 'sumitluitel42@gmail.com'
    message['subject'] = 'You Won!! Congratulations!'
    message.attach(MIMEText(email_msg, 'plain'))
    raw_string =  base64.urlsafe_b64encode(message.as_string().encode()).decode()


    message = service.users().messages().send(userId='me', body={'raw':raw_string}).execute()
    print(message)