from ..firebase.profilestore import ProfileStore
from ..Auth0.user import User
import google.cloud.exceptions
from ..globals import db
import logging
import sys

class EventListStore(object):
    """
    EventListStore class
    This class retrieves and saves Event lists from the
    backend Firebase store
    """
    def __init__(self):
        
        object.__init__(self)

        self.id = ""
        self.events = []
        self.profileStore = ProfileStore()

        logging.debug('Initialize the Events Store')

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

    def getEvents(self, userId):
        """
        getEvents method
        This method retrieve the Events list from Firebase, then constructs full 
        profiles for each Event
        """

        self.id = self.pipe2Underscore(userId)
        reference = db.collection(u'event')
        fieldPath = db.field_path('invited', self.id)
        query = reference.where(fieldPath, u'==', True)

        logging.debug('eventliststore.py, getEvents, Getting events from Google where the path is = {path}'.format(path=fieldPath))
        try:
            self.events = []
            document = query.get() # .to_dict()
            for item in document:
                event = item.to_dict()
                people = list(event['invited'])
                event['invited'] = []
                friends = []
                for person in people:
                    friends.append(self.underscore2Pipe(person))
                logging.debug('eventliststore.py, getEvents, Profiles are {friends}'.format(friends=friends))
                event['invited'] = self.ids2Profiles(friends)
                self.events.append(event)

            # self.id = document['id']
            # self.events = document['events']
            logging.debug('Found events ids for {id} and {events}'.format(id=self.id, events=self.events))
            return { 'events': self.events }
        except google.cloud.exceptions.NotFound as e:
            # TODO: events not found exception
            logging.error('eventliststore.py, getEvents, Events not found {id}'.format(id=self.id))
            logging.error(e)
        except Exception as e:
            logging.error('eventliststore.py, getEvents, Exception when retrieving events for {id}'.format(id=self.id))
            logging.error(e)

    def ids2Profiles(self, friends):
        """
        ids2Profiles method
        Convert a list of members ids to a list of profiles of the members
        """

        logging.debug('eventliststore.py, ids2Profiles, Convert ids to profiles for {ids}'.format(ids=friends))
        profileList = []

        for friend in friends:
            person = self.profileStore.getProfile(friend)

            profile = {
                'id' : person.id,
                'firstName' : person.firstName,
                'lastName' : person.lastName,
                'nickName' : person.nickName,
                'phone' : person.phone,
                'address' : person.address,
                'email' : person.email,
                'newMember' : person.newMember
            }
            profileList.append(profile)
        
        logging.debug('eventliststore.py, ids2Profiles, The friends are {profileList}'.format(profileList=profileList))
        return profileList
