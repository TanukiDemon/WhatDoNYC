from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()
engine = create_engine("sqlite:///users.db")
Session = sessionmaker(bind = engine)

def get_session():
  return Session()

class User(Base): #inherits Base
    __tablename__="User"

    username = Column(String, primary_key=True)
    password = Column(String)
    email = Column(String)
    name = Column(String)
    securityQ = Column(Integer)
    securityQAnswer = Column(String)
    status = Column(Integer)

    def __init__(self, username=None, password=None, email=None, name=None, securityQ=None, answer=None, status=None):
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.securityQ = securityQ # this is an int
        self.securityQAnswer = answer
        self.status = status

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.username)  # python 2
        except NameError:
            return str(self.username)  # python 3

    def __repr__(self):
        return '<User "%d">' % (self.id)
