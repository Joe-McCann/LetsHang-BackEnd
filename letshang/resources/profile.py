"""Profile Resource Submodule"""

import falcon
import json
import logging
from ..firebase.profilestore import ProfileStore
from falcon_cors import CORS

class ProfileResource(object):
    """
    profileResource class
    This class handles the REST API resource for user profiles
    """

    def on_get(self, req, resp, userId):
        """
        on_get method
        This method handles the REST get verb. This function should only be
        invoked by the Falcon framework.

        Arguments:
        req       HTTP request (incoming)
        resp      HTTP response (outgoing)
        userId    The userID of the user's profile passed in the URI
        """
        logging.debug('profile.py, on_get, Get user = {userId}'.format(userId=userId))
        store = ProfileStore()
        store.getProfile(userId)

        # format the response 200
        profile = {
            'id' : store.id,
            'firstName' : store.firstName,
            'lastName' : store.lastName,
            'nickName' : store.nickName,
            'phone' : store.phone,
            'address' : store.address,
            'email' : store.email,
            'newMember' : store.newMember
        }

        resp.body = json.dumps(profile, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp, userId):
        """
        on_put method
        This method handles the REST get verb. This function should only be
        invoked by the Falcon framework.

        Arguments:
        req       HTTP request (incoming)
        resp      HTTP response (outgoing)
        userId    The userID of the user's profile passed in the URI
        """
        logging.debug('profile.py, on_put, Put user = {userId}'.format(userId=userId))

        if req.content_length:
            store = ProfileStore()
            profile = json.loads(req.stream.read().decode('utf-8'))
            store.setAll(profile)
            store.updateProfile()

            # The rest of this is test code
            message = 'The request was successful. UserId = {userId}'.format(userId=profile['id'])
            responseData = { 'message': message }

            resp.body = json.dumps(responseData, ensure_ascii=False)
            resp.status = falcon.HTTP_200
        else:
            message = 'The body of the request must contain profile data'
            responseData = { 'message': message }

            resp.body = json.dumps(responseData, ensure_ascii=False)
            resp.status = falcon.HTTP_400
            return

    def on_post(self, req, resp, userId):
        """
        on_post method
        This method handles the REST get verb. This function should only be
        invoked by the Falcon framework.

        Arguments:
        req       HTTP request (incoming)
        resp      HTTP response (outgoing)
        userId    The userID of the user's profile passed in the URI
        """
        logging.debug('profile.py, on_post, Post user = {userId}'.format(userId=userId))

        if req.content_length:
            store = ProfileStore()
            profile = json.loads(req.stream.read().decode('utf-8'))
            store.setAll(profile)
            store.updateProfile()

            # The rest of this is test code
            message = 'The request was successful. UserId = {userId}'.format(userId=profile['id'])
            responseData = { 'message': message }

            resp.body = json.dumps(responseData, ensure_ascii=False)
            resp.status = falcon.HTTP_200
        else:
            message = 'The body of the request must contain profile data'
            responseData = { 'message': message }

            resp.body = json.dumps(responseData, ensure_ascii=False)
            resp.status = falcon.HTTP_400
            return
