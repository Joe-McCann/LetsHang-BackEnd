"""Map Resource Submodule"""

import falcon
import json

class profileResource(object):
    """
    profileResource class
    This class handles the REST API resource for a map
    """

    def on_get(self, req, resp):
        """
        on_get method
        This method handles the REST get verb. This function should only be
        invoked by the Falcon framework.

        Arguments:
        req       HTTP request (incoming)
        resp      HTTP response (outgoing)
        """

        resp.status = falcon.HTTP_404