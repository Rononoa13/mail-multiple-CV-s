from __future__ import print_function
from email.mime import application
from email.mime import base

from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fileinput import filename
import mimetypes

import base64

import os.path
from random import sample

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def get_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
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
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        return service


    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


def send_message(service, user_id, message):
    message = service.users().messages().send(userId=user_id, body=message).execute() 
    print("Message ID: {}".format(message['id']))

def create_message_with_attachment(sender, to, subject, body, file):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(body)

    content_type, encoding = mimetypes.guess_type(file)
    
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    (main_type, sub_type) = content_type.split('/', 1)

    if main_type == 'text':
        with open(file, 'rb') as f:
            msg = MIMEText(f.read().decode('utf-8'), _subtype=sub_type)

    elif main_type == 'image':
        with open(file, 'rb') as f:
            msg = MIMEImage(f.read(), _subtype=sub_type)

    elif main_type == 'audio':
        with open(file, 'rb') as f:
            msg = MIMEAudio(f.read(), _subtype=sub_type)

    elif main_type == 'aplication'  and sub_type == 'pdf':
        with open(file, 'rb') as f:
            msg = application.MIMEApplication(f.read(), _subtype=sub_type)
    else:
        msg = base.MIMEBase(main_type, sub_type)
        with open(file, 'rb') as f:
            msg.set_payload(f.read())

    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


if __name__ == '__main__':
    
    service = get_service()
    user_id = 'sumitluitel42@gmail.com'
    sender = 'sumitluitel42@gmail.com'
    to = 'sumitluitel91@gmail.com'
    subject = 'IMPORTANT: DO NOT DELETE'
    body = "This is a test subject. Thank you so much for your consideration. Regards."
    file = 'Sumit_Luitel_Resume.pdf'

    msg = create_message_with_attachment(sender, to, subject, body, file)
    send_message(service, user_id, msg)
