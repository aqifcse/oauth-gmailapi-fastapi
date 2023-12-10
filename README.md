# registration
Registration and implementation of Gmail API using Python, Fast API, SQL Alchemy

There are two ways -

Way 1: Gmail Account mail sending
-------------------------------------
1. Place the app/credentials/desktop_client_secret.json 
2. Run the app/first_time.py with the following command
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python app/first_time.py
```
3. This script will pop up a google login screen asking you to give email and password only one time. Once, the login is successfull, there will be an access-refresh-token.json file will be added automatically in the app folder.

4. Now you can then start the server with
```
sudo docker-compose up --build
```

/register api documentation can be found in http://0.0.0.0:8000/docs

giving the credentials a redirecting link will show up in the terminal. click on it and mail will be sent.

Way 2: Service Account
------------------------
If you have a GSUITE admin credentials and the email has domain-wise delegation then place your credentials as service_account_credentials.json in the app/credentials/ folder 

1. Uncomment the 59th and 72th lines in app/main.py and comment out 56 and 69th lines in the same file

after that run the following command - 
```
virtualenv venv
source venv/bin/activate
sudo docker-compose up --build
```


