# registration
Registration and implementation of Gmail API using Python, Fast API, SQL Alchemy


1. Create a service account, take OAuth2 credentials place it to app/credentials/client_secret.json file in the project.
2. place the client id and client secret in docker-compose.yml file


```
virtualenv venv
source venv/bin/activate
sudo docker-compose up --build
```

/register api documentation can be found in http://0.0.0.0:8000/docs

giving the credentials a redirecting link will show up in the terminal. click on it and mail will be sent.
