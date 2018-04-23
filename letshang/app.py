"""API MODULE"""

#from __future__ import absolute_import
#from __future__ import division
#from __future__ import print_function

from .middleware import AuthMiddleware
from .resources.events import eventsResource
from .resources.map import mapResource
from .resources.profile import ProfileResource
from falcon_cors import CORS

import falcon

# This is for running the VS Code interactive debugger
# import waitress

def generic_error_handler(ex, req, resp, params):

    if isinstance(ex, falcon.HTTPNotFound):
        raise falcon.HTTPNotFound(description='Not Found')
    elif isinstance(ex, falcon.HTTPMethodNotAllowed):
        raise falcon.HTTPMethodNotAllowed(falcon.HTTP_405, description='Method Not Allowed')
    else:
        raise ex

cors = CORS(allow_origins_list = ['http://lets-hang.test:9080'])

api = falcon.API(middleware=[ AuthMiddleware(), cors.middleware ])
api.add_route('/events', eventsResource())
api.add_route('/map', mapResource())
api.add_route('/profile/{userId}', ProfileResource())
api.add_error_handler(Exception, generic_error_handler)

# waitress.serve(api, port=8080)
