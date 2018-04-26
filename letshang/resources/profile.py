"""Profile Resource Submodule"""

import falcon
import json
from ..firebase.profilestore import ProfileStore
from falcon_cors import CORS

class ProfileResource(object):
    """
    profileResource class
    This class handles the REST API resource for a map
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