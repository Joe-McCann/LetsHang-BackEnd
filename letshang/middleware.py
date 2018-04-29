"""Middleware Submodule"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import falcon
import logging

class AuthMiddleware(object):
    """."""

    def process_request(self, req, resp):
        if req.method == 'OPTIONS':
            logging.debug('Received an OPTIONS request')
            resp.set_header('Access-Control-Allow-Methods', ','.join(['DELETE','GET','POST','PUT']))
        else:
            token = req.get_header('Authorization')
            logging.debug('Received a {method} request'.format(method=req.method))
            if token is None or not self._token_is_valid():
                logging.warning('Invalid or missing authorization header')
                raise falcon.HTTPUnauthorized(description='Auth token required')

    def _token_is_valid(self):
        return True  # You should do this better!
