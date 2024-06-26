#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    """for DBStorage"""
    cities = relationship('City', backref='state',
                          cascade='all, delete-orphan')
    """getter for file storage"""
    def cities(self):
        return [city for city in models.storage.all(City).values() if
                city.state_id == self.id]
