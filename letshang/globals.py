"""Globals"""
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import json
import requests

cred = credentials.Certificate('./letshang/firebase/letshang-version-000-firebase-adminsdk-4211i-c54a69eb6b.json')
firebase_admin.initialize_app(cred, { 'projectId': 'letshang-version-000', })
db = firestore.client()

def getAuth0Token():

    AUDIENCE = "https://iambillmccann.auth0.com/api/v2/"
    DOMAIN = "iambillmccann.auth0.com"
    CLIENT_ID = "So6wbQdL7oJ5p2cP01oBqp0jr3II9Xk2"
    CLIENT_SECRET = "2D85lAuEub7rp2qDQdPnGP7D-7VZAL-f3QlXbbbZHehcM1mBbnttMhjyOq1EhKf1"
    GRANT_TYPE = "client_credentials" # OAuth 2.0 flow to use

    # Get an Access Token from Auth0
    base_url = "https://{domain}/oauth/token".format(domain=DOMAIN)
    payload = {
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'audience': AUDIENCE,
                'grant_type': GRANT_TYPE
            }

    try:
        r = requests.post(base_url, data=payload)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("Error occured retrieving Auth0 access tokey.")
        print(err)
        return None

    oauth = r.json()
    return oauth['access_token']

token = getAuth0Token