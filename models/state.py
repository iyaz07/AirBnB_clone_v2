#!/usr/bin/python3
""" State Module for HBNB project """
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref
import models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state',cascade='delete')
    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            cities_in_state = []
            for city in list(models.storage.all(City).values()):
                if city.state_id == self.id:
                    cities_in_state.append(city)
            return cities_in_state
