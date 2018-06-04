"""Event Resource Submodule"""

from ..firebase.eventstore import EventStore
import falcon
import json
import logging
from falcon_cors import CORS

class EventResource(object):
    """
    eventResource class
    This class handles the REST API resource for retrieving, adding, changing, or deleting a single event.
    """

    def on_post(self, req, resp, eventId):
        """
        on_post method
        This method handles the REST post verb.
        """
        logging.debug('event.py, on_post, Method start event = {eventId}'.format(eventId=eventId))

        if req.content_length:
            store = EventStore()
            event = json.loads(req.stream.read().decode('utf-8'))

            # TODO. Do something
            store.NewEvent(event)

            message = 'The request was successful. Event Id = {eventId}'.format(eventId=eventId)
            responseData = { 'message': message }

            resp.body = json.dumps(responseData, ensure_ascii=False)
            resp.status = falcon.HTTP_200
        else:
            message = 'The body of the request must contain profile data'
            responseData = { 'message': message }

            resp.body = json.dumps(responseData, ensure_ascii=False)
            resp.status = falcon.HTTP_400
            return
        
