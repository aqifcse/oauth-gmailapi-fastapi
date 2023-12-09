from fastapi import FastAPI, BackgroundTasks, HTTPException
from .services import create_service_with_client_secret, create_service_with_service_account
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi.middleware.cors import CORSMiddleware
from .expired_date import convert_iso_to_dhaka_time
from typing import Optional

import bcrypt
#the following line of code are to import the user in our model and schema
from .models import User as ModelUser
from .schemas import User
from .schemas import User as Users
from .db import SessionLocal, Base, engine

# Create tables based on the models
Base.metadata.create_all(bind=engine)
# Dependency

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

def send_email_background(user: User):
  emailMsg = 'Welcome!!'
  mimeMessage = MIMEMultipart()
  mimeMessage['to'] = user.email
  mimeMessage['subject'] = 'Your account has been created!!!'
  mimeMessage.attach(MIMEText(emailMsg, 'plain'))
  raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

  try:
    # Send Mail
    service= create_service_with_client_secret(CLIENT_SECRET_FILE, APPLICATION_NAME, API_NAME, API_VERSION, SCOPES)
    
    # For Service account 
    # service = create_service_with_service_account(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    return service.users().messages().send(userId='me', body={'raw': raw_string}).execute()

  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))
  
def send_email_background_during_technical_difficulty(user):
  try:
    # Send Mail
    service= create_service_with_client_secret(CLIENT_SECRET_FILE, APPLICATION_NAME, API_NAME, API_VERSION, SCOPES)
    
    # For Service account 
    # service = create_service_with_service_account(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    emailMsg = "Sorry, Due to some technical difficulty your registration was not successful. Please re-register"
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = user.email
    mimeMessage['subject'] = 'Your registration is not successful'
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    return service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))



    
    
db = SessionLocal() 

def database_user_create(user: User):
 
  # creating user in the database
  hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
  user = ModelUser(username=user.username, email=user.email, password=hashed_password, full_name=user.full_name, disabled=user.disabled)
  db.add(user)
  db.commit()
  db.refresh(user)

  if user.id:
    return user
  else:
    raise HTTPException(status_code=500, detail="Failed to create user")
   
   

@app.post("/register")
async def create_user(user: User, background_tasks: BackgroundTasks):

  try:
    # creating user in the database
    stored_user = database_user_create(user)
    # sending email as a background task
    background_tasks.add_task(
      send_email_background, stored_user
    )

    expired_date = convert_iso_to_dhaka_time()

    response = { "message":"Success!! Successfully registered. Welcome email sent. Email sending token will be expired at " + expired_date }
    return response
  except Exception as e:
    background_tasks.add_task(
      send_email_background_during_technical_difficulty, user
    )
    return HTTPException(status_code=400, detail=str(e))
    

