"""Profile Store Submodule"""
from ..Auth0.user import User
import google.cloud.exceptions
from ..globals import db

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

        try:
            document = reference.get().to_dict()

            self.firstName = document['firstName']
            self.lastName = document['lastName']
            self.nickName = document['nickName']
            self.phone = document['phone']
            self.address = document['address']
            self.email = document['email']
            self.newMember = False
            
        except google.cloud.exceptions.NotFound:
            # First we call Auth0 to obtain the user profile
            auth0User = User()
            auth0User.getUser(userId)

            # Then we set the object properties
            self.firstName = auth0User.firstName
            self.lastName = auth0User.lastName
            self.email = auth0User.email
            self.nickName = auth0User.nickName

            # Then we write the object back to Firebase
            self.addProfile()

        # Finally we return the profile object    
        return self

    def addProfile(self):
        """
        addProfile method
        This function stores the current object properties in the Google Cloud Firestore.
        Use this method for adding new records to the database
        """

        db.collection(u'people').document(self.id).set(self.asJson())

    def updateProfile(self):
        """
        updateProfile method
        This function updates a document (record) that is already stored on Firestore.
        """

        reference = db.collection(u'people').document(self.id)
        reference.update(self.asJson())

    def deleteProfile(self, userId):
        """
        deleteProfile method
        This function delete a document from Firestore
        """

        try:
            db.collection(u'people').document(userId).delete()
        except google.cloud.exceptions.NotFound:
            print("Nothing to delete, id = {userId}".format(userId=userId))

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
        