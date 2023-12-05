from fastapi import FastAPI
from google.oauth2 import service_account
from googleapiclient.discovery import build
from .service import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi.responses import HTMLResponse, RedirectResponse

CLIENT_SECRET_FILE = 'app/client_secret.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

app = FastAPI()

@app.post("/register/")
async def resgister(fullname: str, email: str, password: str):
  service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

  emailMsg = 'Welcome!!' + fullname
  mimeMessage = MIMEMultipart()
  mimeMessage['to'] = email
  mimeMessage['subject'] = 'Your account has been created!!!'
  mimeMessage.attach(MIMEText(emailMsg, 'plain'))
  raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

  message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
  return RedirectResponse(message)