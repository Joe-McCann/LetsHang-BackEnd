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
    def __init__(self, userId):
        
        object.__init__(self)

        self.id = userId
        self.friends = []

        logging.debug('Initialize the Friends Store')

    def saveFriends(self, friends):
        """
        saveFriends method
        This method determines whether to add to Firebase or to update Firebase
        """

        self.friends = friends

        reference = db.collection(u'friends').document(self.id)
        logging.debug('Updateing friends on Google = {id}'.format(id=self.id))

        try:
            reference.update(self.asJson())
        except google.cloud.exceptions.NotFound:
            logging.debug('User not found userId = {userId}'.format(userId=self.id))
            self.newFriends()
            
        return self

    def newFriends(self):
        """
        newFriends method
        This method creates a document of friends when a user is created. The initial friends list
        is empty
        """

        reference = db.collection(u'friends').document(self.id)
        logging.debug('Adding friends to Google = {id}'.format(id=self.id))

        try:
            db.collection(u'friends').document(self.id).set(self.asJson())            
        except Exception as e:
            logging.error('Exception when adding friends for {id}'.format(id=self.id))
            logging.error(e)

        return self


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
