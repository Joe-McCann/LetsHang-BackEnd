"""Event/Friends Resource Submodule"""

from ..firebase.eventstore import EventStore
import falcon
import json
import logging
from falcon_cors import CORS

class EventFriendsResource(object):
    """
    EventFriendsResource class
    This class handles the REST API resource for retrieving, adding, changing, or deleting a single event for a
    specific user.
    """

    def __init__(self):
        
        object.__init__(self)

        logging.debug('eventFriends.py, __init__, Creating an EventFriends object')
        self.store = EventStore()

    def on_delete(self, req, resp, eventId, userId):
        """
        on_post method
        This method handles the REST post verb.
        """
        logging.debug('eventFriends.py, on_delete, event = {eventId} and user = {userId}'.format(eventId=eventId, userId=userId))
        event = self.store.GetEvent(eventId)
