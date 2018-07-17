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

        logging.debug('profilestore.py, __init__, Initialize the Profile Store')

    def notFromUs(self, userId):
        """
        notNewSignup method
        check to see if the member id was created by Lets-Hang
        """
        if userId.split("|")[0].lower() != "LETSHANG":
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

        logging.debug('profilestore.py, getProfile, Getting from Google = {id}'.format(id=self.id))

        try:
            document = reference.get().to_dict()
            logging.debug('profilestore.py, getProfile, getProfile retrieved {document} from Firebase'.format(document=document))
            self.firstName = document['firstName']
            self.lastName = document['lastName']
            self.nickName = document['nickName']
            self.phone = document['phone']
            self.address = document['address']
            self.email = document['email']
            self.newMember = False
            logging.debug('profilestore.py, getProfile, User found {firstname} {lastname}'.format(firstname=self.firstName, lastname=self.lastName))
            
        except google.cloud.exceptions.NotFound:
            # First we call Auth0 to obtain the user profile
            logging.debug('profilestore.py, getProfile, User not found in getProfile userId = {userId}'.format(userId=userId))
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

        logging.debug('profilestore.py, addProfile, Adding to Google = {id}'.format(id=self.id))        

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
        logging.debug('profilestore.py, add2Firebase, In add2Firebase id = {userId}'.format(userId=self.id))
        db.collection(u'people').document(self.id).set(self.asJson())

        # We're not done yet. If this new profile is a new member registering, then we must
        # also give them a friend list. We determine this by scanning the user id.
        if self.notFromUs(self.id):
            logging.debug('profilestore.py, add2Firebase, In add2Firebase checked notFromUs id = {userId}'.format(userId=self.id))
            store = FriendListStore()
            store.newFriends(self.id)

    def updateProfile(self):
        """
        updateProfile method
        This function updates a document (record) that is already stored on Firestore.
        """

        reference = db.collection(u'people').document(self.id)

        logging.debug('profilestore.py, updateProfiles, Updating on Google = {id}'.format(id=self.id))

        try:
            reference.update(self.asJson())
        except google.cloud.exceptions.NotFound:
            logging.debug('profilestore.py, updateProfiles, User not found in updateProfile userId = {userId}'.format(userId=self.id))
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
            logging.error("profilestore.py, deleteProfile, Nothing to delete, id = {userId}".format(userId=userId))

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

    def ids2Profiles(self, friendIds):
        """
        ids2Profiles method
        Convert a list of members ids to a list of profiles of the members
        """

        logging.debug('profilestore.py, ids2Profiles, Convert ids to profiles for {ids}'.format(ids=friendIds))

        profileList = []
        if friendIds == None:
            return profileList   # If there are not friends, then return an empty list

        userId = friendIds['id']
        friends = friendIds['friends']

        for friend in friends:
            self.getProfile(friend)

            profile = {
                'id' : self.id,
                'firstName' : self.firstName,
                'lastName' : self.lastName,
                'nickName' : self.nickName,
                'phone' : self.phone,
                'address' : self.address,
                'email' : self.email,
                'newMember' : self.newMember
            }
            profileList.append(profile)
        
        logging.debug('profilestore.py, ids2Profiles, The friends are {profileList}'.format(profileList=profileList))
        return profileList
        