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

    def GetEvent(self, id):
        """
        GetEvent retrieves an event from Firebase
        """

        logging.debug('eventstore.py, GetEvent, Get event {id}'.format(id=id))
        self.id = id
        reference = db.collection(u'event').document(self.id)
        try:
            event = reference.get().to_dict()
            logging.debug('eventstore.py, getEvent, returned from Firebase {event}'.format(event=event))
            self.SetDesc(event)
            people = list(event['invited'])
            self.invited = []
            for person in people:
                self.invited.append(self.underscore2Pipe(person))
            logging.debug('eventstore.py, getEvents, Invited are {invited}'.format(invited=self.invited))
            return self
        except Exception as e:
            logging.error('eventstore.py, GetEvent, Exception when retrieving event for {id}'.format(id=self.id))
            logging.error(e)
            return self

    def RemovePerson(self, userId):
        """
        RemovePerson deletes an invited person from the invited list
        """

        self.invited.remove(userId)
        logging.debug('eventstore.py, RemovePerson, Invited are {invited}'.format(invited=self.invited))

    def SetAll(self, event):
        """
        SetAll set event variables from an event object
        """

        logging.debug('eventstore.py, SetDesc, In the SetAll method')
        self.SetDesc(event)
        self.invited = self.idDict(event['invited'])

    def SetDesc(self, event):
        """
        SetDesc sets the event description variables from an event object
        """
        
        self.id = event['id']
        logging.debug('eventstore.py, SetDesc, Setting values for {id}'.format(id=self.id))
        self.eventDescription = event['eventDescription']
        self.date = event['date']
        self.time = event['time']
        
    def idDict(self, invited):
        """
        idDict method
        This function returns a dictionary of ids from a list of profiles. The dictionary
        contains a single value of True that is used by Firebase to perform queries
        against the list.
        """

        logging.debug('eventstore.py, idDict, In idDict with {invited}'.format(invited=invited))
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
            logging.error('eventstore.py, NewEvent, Exception when adding event for {id}'.format(id=self.id))
            logging.error(e)

        return self

    def UpdateEvent(self):
        """
        newEvent method
        This method updates an event. NOTE! The event data must already be stored this the class variables!
        """

        logging.debug('eventstore.py, UpdateEvent, In UpdateEvent with {id}'.format(id=self.id))
        reference = db.collection(u'event').document(self.id)

        try:
            reference.update(self.asJson())            
        except Exception as e:
            logging.error('eventstore.py, NewEvent, Exception when adding event for {id}'.format(id=self.id))
            logging.error(e)

        return self

    def DeleteEvent(self):
        """
        deleteEvent method
        This function deletes an event from Firestore. NOTE! The event must already stored in this class.
        """

        logging.debug('eventstore.py, DeleteEvent, In DeleteEvent with {id}'.format(id=self.id))
        reference = db.collection(u'event').document(self.id)

        try:
            reference.delete()
        except google.cloud.exceptions.NotFound:
            logging.error("eventstore.py, deleteevent, Nothing to delete, id = {userId}".format(userId=userId))

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

    def underscore2Pipe(self, key):
        """
        underscore2Pipe
        This method replaces the underscore needed in the eventlist with the pipe character used
        by auth0 ids. Let's Hang uses the auth0 key for ids.
        7/2/2018: Adding support for the google-oauth keyword.
        """
        newKey = key.replace("google_oauth2", "google-oauth2", 1)
        return newKey.replace("_", "|", 1)

    def pipe2Underscore(self, key):
        """
        pipe2Underscore
        This method replace the pipe in an id with an underscore. This enables querying on the id.
        7/2/2018: Adding support for the google-oauth keyword.
        NOTE: This method is a copy of the pipe2Underscore in eventstore.py
        """
        newKey = key.replace("google-oauth2", "google_oauth2", 1)
        return newKey.replace("|", "_", 1)
