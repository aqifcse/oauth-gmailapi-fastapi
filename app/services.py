import pickle
import os
from fastapi import HTTPException, Request
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import oauth2client
from oauth2client import client, tools, file


def get_credentials(client_secret_file, application_name, *scopes):
    home_dir = os.path.expanduser('~')
    credential_dir = 'app/credentials/'
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'access-refresh-token.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secret_file, scopes)
        flow.user_agent = application_name
        credentials = tools.run_flow(flow, store)
    return credentials



def create_service_with_client_secret(client_secret_file, application_name, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    APPLICATION_NAME = application_name
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or cred.invalid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            # flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            # cred = flow.run_local_server(host='localhost', port=8080, open_browser=False)

            # Tell the user to go to the authorization URL.
            # auth_url, _ = flow.authorization_url(prompt='consent')

            cred = get_credentials(CLIENT_SECRET_FILE, APPLICATION_NAME, SCOPES)

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        return service
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Need a GSUITE Admin created service account for using this function. please check the details - https://developers.google.com/identity/protocols/oauth2/service-account#delegatingauthority
def create_service_with_service_account(client_secret_file, api_name, api_version, *scopes):
    SERVICE_ACCOUNT_CREDENTIALS_JSON_PATH = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_CREDENTIALS_JSON_PATH,
        SCOPES
    )

    del_credentials = credentials.with_subject('xyz@example.com')

    service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    return service 

