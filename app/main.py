from fastapi import FastAPI
from .services import create_service_with_client_secret, create_service_with_service_account
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi.middleware.cors import CORSMiddleware
from .expired_date import convert_iso_to_dhaka_time

import bcrypt
#the following line of code are to import the user in our model and schema
from .models import User as ModelUser
from .schemas import User
from .schemas import User as Users
from .db import SessionLocal, Base, engine

# Create tables based on the models
Base.metadata.create_all(bind=engine)
# Dependency

db = SessionLocal()

CLIENT_SECRET_FILE = 'app/credentials/desktop_client_secret.json'
APPLICATION_NAME = 'fastapi-registration'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

origins = [
  "http://0.0.0.0:8000",
  "http://localhost:8080",
  "https://accounts.google.com",
  "https://gmail.googleapis.com"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register")
async def create_user(user: User):

  # creating user in the database
  hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
  user = ModelUser(username=user.username, email=user.email, password=hashed_password, full_name=user.full_name, disabled=False)
  db.add(user)
  db.commit()
  db.refresh(user)

  # Send Mail
  service= create_service_with_client_secret(CLIENT_SECRET_FILE, APPLICATION_NAME, API_NAME, API_VERSION, SCOPES)
  # service = create_service_with_service_account(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

  emailMsg = 'Welcome!!' + user.full_name
  mimeMessage = MIMEMultipart()
  mimeMessage['to'] = user.email
  mimeMessage['subject'] = 'Your account has been created!!!'
  mimeMessage.attach(MIMEText(emailMsg, 'plain'))
  raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

  # Send mail using the service 
  service.users().messages().send(userId='me', body={'raw': raw_string}).execute()

  expired_date = convert_iso_to_dhaka_time()

  response = { "message":"Success!! Successfully registered. Email sending token will be expired at " + expired_date }
  return response
