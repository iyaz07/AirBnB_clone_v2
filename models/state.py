#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref
from os import getenv
import models

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == 'db':
        """for DBStorage"""
        cities = relationship('City', backref='state',
                          cascade='all, delete-orphan')
    else:
        @property
        def cities(self):
            """ getter for Filestorage """
            import models
            from models.city import City
            return [city for city in models.storage.all(City).values() if
                city.state_id == self.id]
