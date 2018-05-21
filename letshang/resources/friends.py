"""Friends Resource Submodule"""

import falcon
import json
import logging
from ..firebase.friendliststore import FriendListStore
from falcon_cors import CORS

class FriendsResource(object):
    """
    friendsResource class
    This class handles the REST API resource for a list of friends
    """

    def on_get(self, req, resp, userId):
        """
        on_get method
        This method handles the REST get verb. This function should only be
        invoked by the Falcon framework.

        Arguments:
        req       HTTP request (incoming)
        resp      HTTP response (outgoing)
        userId    The userID for the person whose friends are retrieved
        """
        logging.debug('Get friends = {userId}'.format(userId=userId))

        # format the response 200
        friendlist = {
            'id' : userId,
            'friends' : []
        }

        resp.body = json.dumps(friendlist, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp, userId):
        """
        on_post method
        This method handles the REST get verb. This function should only be
        invoked by the Falcon framework.

        Arguments:
        req       HTTP request (incoming)
        resp      HTTP response (outgoing)
        userId    The userID of the user's friend list passed in the URI
        """
        logging.debug('Put friend lsit = {userId}'.format(userId=userId))

        if req.content_length:
            store = FriendListStore(userId)
            friends = json.loads(req.stream.read().decode('utf-8'))
            store.saveFriends(friends)
        else:
            message = 'The body of the request must contain a list of friends'
            responseData = { 'message': message }

            resp.body = json.dumps(responseData, ensure_ascii=False)
            resp.status = falcon.HTTP_400
            return
            