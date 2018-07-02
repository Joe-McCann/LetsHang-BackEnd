"""Profile Store Submodule"""
import google.cloud.exceptions
from ..firebase.friendliststore import FriendListStore
from ..globals import db
import logging
import json

class EventStore(object):
    """
    EventStore class
    This class retrieves and saves event data from the
    backend Firebase store
    """

    def __init__(self):
        
        object.__init__(self)

        logging.debug('eventstore.py, __init__, Creating an EventStore object')
        self.id = ""
        self.eventDescription = ""
        self.date = ""
        self.time = ""
        self.invited = []

    def SetAll(self, event):
        """
        SetAll set event variables from an event object
        """

        self.id = event['id']
        logging.debug('eventstore.py, SetAll, Setting values for {id}'.format(id=self.id))
        self.eventDescription = event['eventDescription']
        self.date = event['date']
        self.time = event['time']
        
        self.invited = self.idDict(event['invited'])

    def idDict(self, invited):
        """
        idDict method
        This function returns a dictionary of ids from a list of profiles. The dictionary
        contains a single value of True that is used by Firebase to perform queries
        against the list.
        """

        logging.debug('eventsote.py, idDict, In idDict with {invited}'.format(invited=invited))
        ids = {}
        for profile in invited:
            ids[ self.pipe2Underscore(profile['id']) ] = True

        return ids

    def NewEvent(self, event):
        """
        newEvent method
        This method creates a document for an event
        """

        self.SetAll(event)
        logging.debug('eventstore.py, NewEvent, In NewEvent with {id}'.format(id=self.id))
        reference = db.collection(u'event').document(self.id)

        try:
            reference.set(self.asJson())            
        except Exception as e:
            logging.error('Exception when adding event for {id}'.format(id=self.id))
            logging.error(e)

        return self

    def asJson(self):
        """
        asJson method
        This function compiles the class variables into JSON.
        """

        data = {
           'id': self.id,
           'eventDescription': self.eventDescription,
           'date': self.date,
           'time': self.time,
           'invited': self.invited
        }
        return data

    def pipe2Underscore(self, key):
        """
        pipe2Underscore
        This method replace the pipe in an id with an underscore. This enables querying on the id.
        7/2/2018: Adding support for the google-oauth keyword.
        NOTE: This method is a copy of the pipe2Underscore in eventstore.py
        """
        newKey = key.replace("google-oauth2", "google_oauth2", 1)
        return newKey.replace("|", "_", 1)
