from .models import get_session, User
from sqlalchemy import *
class logUser(object):
    def __init__(self):
        self.is_authenticated = False
        self.is_active = True
        self.is_anonymous = False
        self.username = ""

    def get_id(self):
        sqliteSession = get_session()
        result = sqliteSession.execute('SELECT rowid FROM User WHERE username = :uname', {'uname': self.username})
        return str(result).encode("utf-8").decode("utf-8")
        #This method must return a unicode that uniquely identifies this user,
        #and can be used to load the user from the user_loader callback. Note that
        # this must be a unicode - if the ID is natively an int or some other type,
        # you will need to convert it to unicode.
