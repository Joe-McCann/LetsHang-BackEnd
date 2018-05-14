"""Friends Resource Submodule"""

import falcon
import json
import logging
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
        profile = {
            'id' : userId,
            'friends' : []
        }

        resp.body = json.dumps(profile, ensure_ascii=False)
        resp.status = falcon.HTTP_200
