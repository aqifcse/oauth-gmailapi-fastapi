import os
import oauth2client
from oauth2client import client, tools, file

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