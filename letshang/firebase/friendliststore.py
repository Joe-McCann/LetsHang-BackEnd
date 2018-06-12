"""Profile Store Submodule"""
from ..Auth0.user import User
import google.cloud.exceptions
from ..globals import db
import logging
import sys

class FriendListStore(object):
    """
    FriendListStore class
    This class retrieves and saves friend lists from the
    backend Firebase store
    """
    def __init__(self):
        
        object.__init__(self)

        self.id = ""
        self.friends = []

        logging.debug('Initialize the Friends Store')

    def getFriends(self, userId):
        """
        getFriends method
        This method retrieves the friends list from Firebase, then constructs full 
        profiles for each friend
        """

        # Make a call to Firebase to retrieve the user
        # userId = userId.encode("utf-8")
        self.id = userId
        reference = db.collection(u'friends').document(self.id)

        logging.debug('Getting friends from Google = {id}'.format(id=self.id))
        try:
            document = reference.get().to_dict()
            logging.debug('Friends returns from Firebase {document}'.format(document=document))
            self.id = document['id']
            self.friends = document['friends']
            logging.debug('Found friend ids for {id} and {friends}'.format(id=self.id, friends=self.friends))
            return document
        except google.cloud.exceptions.NotFound as e:
            # TODO: friends not found exception
            logging.error('Friends not found {id}'.format(id=self.id))
            logging.error(e)
        except Exception as e:
            logging.error('Exception when retrieving friends for {id}'.format(id=self.id))
            logging.error(e)

    def saveFriends(self, friendList):
        """
        saveFriends method
        This method determines whether to add to Firebase or to update Firebase
        """

        self.id = friendList['id']
        self.friends = self.idOnly(friendList['friends'])

        reference = db.collection(u'friends').document(self.id)
        logging.debug('Updateing friends on Google = {id}'.format(id=self.id))

        try:
            reference.update(self.asJson())
        except google.cloud.exceptions.NotFound:
            logging.debug('User not found in saveFriends userId = {userId}'.format(userId=self.id))
            self.newFriends(self.id)
            
        return self

    def newFriends(self, userId):
        """
        newFriends method
        This method creates a document of friends when a user is created. The initial friends list
        is empty
        """

        self.id = userId
        logging.debug('In newFriends with {id} and {userId}'.format(id=self.id, userId=userId))
        reference = db.collection(u'friends').document(self.id)
        logging.debug('Adding friends to Google = {id}'.format(id=self.id))

        try:
            db.collection(u'friends').document(self.id).set(self.asJson())            
        except Exception as e:
            logging.error('Exception when adding friends for {id}'.format(id=self.id))
            logging.error(e)

        return self

    def idOnly(self, friends):
        """
        idOnly method
        This function returns a list of ids from a list of profiles
        """

        logging.debug('friendliststore.py, idOnly, In idOnly with {friends}'.format(friends=friends))
        ids = []
        for profile in friends:
            ids.append(profile['id'])

        return ids

    def asJson(self):
        """
        asJson method
        This function compiles the class variables into JSON.
        """

        data = {
            'id': self.id,
            'friends': self.friends
        }

        return data
