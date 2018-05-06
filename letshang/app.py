"""API MODULE"""

from .middleware import AuthMiddleware
from .resources.events import eventsResource
from .resources.map import mapResource
from .resources.profile import ProfileResource
from falcon_cors import CORS

import falcon
import logging

logging.basicConfig(filename='letshang-backend.log', level=logging.DEBUG)
logging.info('*** Starting the Let\'s Hang Server ***')

#!!! This is for running the VS Code interactive debugger
# import waitress

def generic_error_handler(ex, req, resp, params):

    if isinstance(ex, falcon.HTTPNotFound):
        raise falcon.HTTPNotFound(description='Not Found')
    elif isinstance(ex, falcon.HTTPMethodNotAllowed):
        raise falcon.HTTPMethodNotAllowed(falcon.HTTP_405, description='Method Not Allowed')
    else:
        raise ex

cors = CORS(allow_all_origins=True,
            allow_all_headers=True,
            allow_methods_list=['DELETE','GET','POST','PUT'])

api = falcon.API(middleware=[ cors.middleware, AuthMiddleware() ])
api.add_route('/events', eventsResource())
api.add_route('/map', mapResource())
api.add_route('/profile/{userId}', ProfileResource())
# api.add_route('/mapMaker', mapMaker())
api.add_error_handler(Exception, generic_error_handler)

#!!! This is for running the VS Code interactive debugger
# waitress.serve(api, port=8080)
logging.debug('app.py, Application housekeeping completed')
