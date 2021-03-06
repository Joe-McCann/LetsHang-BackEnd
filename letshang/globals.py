"""Globals"""
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import json
import requests
import logging

cred = credentials.Certificate('./letshang/firebase/letshang-v000-firebase-adminsdk-44oaf-cfef7bae9e.json')
firebase_admin.initialize_app(cred, { 'projectId': 'letshang-v000', })
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
        logging.error("globals.py, getAuth0Token, Error occured retrieving Auth0 access token.")
        logging.error(err)
        return None

    oauth = r.json()
    return oauth['access_token']

token = getAuth0Token()
