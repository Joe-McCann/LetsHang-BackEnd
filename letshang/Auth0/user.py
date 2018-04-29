"""Auth0 user profile sub-module"""
import requests
import logging
from ..globals import token

class User(object):
    """
    User class
    This class returns the user profile from Auth0
    """
    def __init__(self):
        self.firstName = ""
        self.lastName = ""
        self.nickName = ""
        self.email = ""

    def getUser(self, userId):
        """
        getUser method
        This method retrieves the profile data from Auth0. This is only
        done when the user is new to letshang.

        Arguments:
        userId   The auth0 userId pass from the letshang app
        """
        if token == None: return
        base_url = "https://iambillmccann.auth0.com/api/v2/users/{user}".format(user=userId)
        headers = {'Authorization': 'Bearer {cred}'.format(cred=token)}

        logging.debug('In getUser')

        try:
            r = requests.get(base_url, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logging.error("Error occured retrieving Auth0 normalized user profile.")
            logging.error(err)
            return self

        payload = r.json()
        logging.debug('In user, returned from Auth0')

        try:
            self.firstName = payload['given_name']
        except KeyError as err:
            self.firstName = ""
        try:
            self.lastName = payload['family_name']
        except KeyError as err:
            self.lastName = ""
        try:
            self.nickName = payload['nickname']
        except KeyError as err:
            self.nickName = ""
        try:
            self.email = payload['email']
        except KeyError as err:
            self.email = ""

        return self
        