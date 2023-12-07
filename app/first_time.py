import httplib2
import os
import oauth2client
from oauth2client import client, tools, file
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
import mimetypes
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase

SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'app/credentials/desktop_client_secret.json'
APPLICATION_NAME = 'fastapi-registration'

# https://stackoverflow.com/questions/37201250/sending-email-via-gmail-python
def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = 'credentials/'
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'access-refresh-token.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
    return credentials

def main():
    get_credentials()

if __name__ == '__main__':
    main()