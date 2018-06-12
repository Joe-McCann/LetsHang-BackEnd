"""Events Resource Submodule"""

import falcon
import json
import logging
from ..firebase.eventliststore import EventListStore

class eventsResource(object):
    """
    eventsResource class
    This class handles the REST API resource for events.
    """
    def __init__(self):
        
        object.__init__(self)

        logging.debug('events.py, __init__, Creating an Event object')
        self.store = EventListStore()

    def on_get(self, req, resp, userId):
        """
        on_get method
        This method handles the REST get verb. This function should only be
        invoked by the Falcon framework.

        Arguments:
        req       HTTP request (incoming)
        resp      HTTP response (outgoing)

        Currently this method returns a hardcoded response. The response event list contains
        two events and each event contains two people.
        """
        logging.debug('events.py, on_get, Get events = {userId}'.format(userId=userId))
        
        # Hardcoding the resource until Firebase is hooked in.
        events = self.store.getEvents(userId)

        resp.body = json.dumps(events, ensure_ascii=False)
        resp.status = falcon.HTTP_200