from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

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
    def __repr__(self):
        return '<User "%d">' % (self.id)
