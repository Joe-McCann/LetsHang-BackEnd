"""Profile Store Submodule"""
from ..Auth0.user import User
import google.cloud.exceptions
from ..firebase.friendliststore import FriendListStore
from ..globals import db
import logging

class ProfileStore(object):
    """
    profileStore class
    This class retrieves and saves profile data from the
    backend Firebase store
    """
    def __init__(self):
        
        object.__init__(self)

        self.id = ""
        self.firstName = ""
        self.lastName = ""
        self.nickName = ""
        self.address = ""
        self.phone = ""
        self.email = ""
        self.newMember = True

        logging.debug('Initialize the Profile Store')

    def notFromUs(self, userId):
        """
        notNewSignup method
        check to see if the member id was created by Lets-Hang
        """
        if userId.split("|")[0].lower() != "lets-hang":
            return True
        return False

    def setAll(self, profile):
        """
        setAll method
        This method will set all the values of the class based on an
        object with similar properties
        """

        self.id = profile['id']
        self.firstName = profile['firstName']
        self.lastName = profile['lastName']
        self.nickName = profile['nickName']
        self.address = profile['address']
        self.phone = profile['phone']
        self.email = profile['email']
        self.newMember = False

    def getProfile(self, userId):
        """
        getProfile method
        This method attempts to retreive a user's profile
        from Firebase. It sets default values if the profile
        is not found.

        Arguments:
        userId     The userId as provided by Auth0
        """
        # Make a call to Firebase to retrieve the user
        # userId = userId.encode("utf-8")
        self.id = userId
        reference = db.collection(u'people').document(self.id)

        logging.debug('Getting from Google = {id}'.format(id=self.id))

        try:
            document = reference.get().to_dict()
            self.firstName = document['firstName']
            self.lastName = document['lastName']
            self.nickName = document['nickName']
            self.phone = document['phone']
            self.address = document['address']
            self.email = document['email']
            self.newMember = False
            logging.debug('User found {firstname} {lastname}'.format(firstname=self.firstName, lastname=self.lastName))
            
        except google.cloud.exceptions.NotFound:
            # First we call Auth0 to obtain the user profile
            logging.debug('User not found userId = {userId}'.format(userId=userId))
            auth0User = User()
            auth0User.getUser(userId)

            # Then we set the object properties
            self.firstName = auth0User.firstName
            self.lastName = auth0User.lastName
            self.email = auth0User.email
            self.nickName = auth0User.nickName

            # Then we write the object back to Firebase
            self.add2Firebase()

        # Finally we return the profile object    
        return self

    def addProfile(self):
        """
        updateProfile method
        This function updates a document (record) that is already stored on Firestore.
        """

        reference = db.collection(u'people').document(self.id)

        logging.debug('Adding to Google = {id}'.format(id=self.id))        

        try:
            self.add2Firebase()
        except google.cloud.exceptions.Error:
            logging.debug('Problem saving userId = {userId}'.format(userId=self.id))
            
        return self

    def add2Firebase(self):
        """
        add2Firebase method
        This function stores the current object properties in the Google Cloud Firestore.
        Use this method for adding new records to the database
        """

        db.collection(u'people').document(self.id).set(self.asJson())

        # We're not done yet. If this new profile is a new member registering, then we must
        # also give them a friend list. We determine this by scanning the user id.
        if self.notFromUs(self.id):
            store = FriendListStore(self.id)
            store.newFriends()

    def updateProfile(self):
        """
        updateProfile method
        This function updates a document (record) that is already stored on Firestore.
        """

        reference = db.collection(u'people').document(self.id)

        logging.debug('Updating on Google = {id}'.format(id=self.id))

        try:
            reference.update(self.asJson())
        except google.cloud.exceptions.NotFound:
            logging.debug('User not found userId = {userId}'.format(userId=self.id))
            self.add2Firebase()
            
        return self

    def deleteProfile(self, userId):
        """
        deleteProfile method
        This function delete a document from Firestore
        """

        try:
            db.collection(u'people').document(userId).delete()
        except google.cloud.exceptions.NotFound:
            logging.error("Nothing to delete, id = {userId}".format(userId=userId))

    def asJson(self):
        """
        asJson method
        This function compiles the class variables into JSON.
        """

        data = {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'nickName': self.nickName,
            'address': self.address,
            'email': self.email,
            'phone': self.phone
        }
        return data
        