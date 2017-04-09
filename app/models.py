from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from werkzeug.security import generate_password_hash

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
    securityQ = Column(Int)
    securityQAnswer = Column(String)

    def __init__(self, username, password, email, name, securityQ, answer):
        self.username = str(username)
        self.set_password(str(password))
        self.email = str(email)
        self.name = str(name)
        self.securityQ = int(securityQ)
        self.securityQAnswer = str(answer)


    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)


    def __repr__(self):
        return '<User "%d">' % (self.id)
