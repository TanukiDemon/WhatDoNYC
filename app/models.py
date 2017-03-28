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
    __tablename__="userAuthen"

    username = Column(String, primary_key=True)
    password = Column(String)
    email = Column(String)
    firstName = Column(String)

    def __init__(self, username, passowrd, email, firstName):
        self.username = username
        self.set_password(password)
        self.email = email
        self.firstname = firstname

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)


    def __repr__(self):
        return '<User "%d">' % (self.id)
