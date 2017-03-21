from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///msgdetect.db")
Session = sessionmaker(bind = engine)

def get_session():
  return Session()

class User(Base): #inherits Base
    __tablename__="users"

    id = Column(Integer, primary_key=True)
    device = Column(String(120))
    accel_readings = relationship('Accelerometer', backref='user', lazy='dynamic')
    keyboard_readings = relationship('Keyboard', backref='user', lazy='dynamic')
    def __repr__(self):
        return '<User "%d">' % (self.id)
