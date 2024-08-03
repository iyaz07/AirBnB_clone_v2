#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

time = "%Y-%m-%dT%H:%M:%S.%f"

# Create a base class for all models
Base = declarative_base()

class BaseModel:
    """A base class for all hbnb models"""

    # Define columns for the base model
    id = Column(String(60), primary_key=True, nullable=False, default=str(uuid.uuid4()))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        # Initialize default values for id, created_at, and updated_at
        if not kwargs.get('id'):
            self.id = str(uuid.uuid4())
        if not kwargs.get('created_at'):
            self.created_at = datetime.utcnow()
        if not kwargs.get('updated_at'):
            self.updated_at = datetime.utcnow()

        # Update attributes from kwargs if provided
        if kwargs:
            for key, value in kwargs.items():
                if key in ['created_at', 'updated_at']:
                    # Convert string to datetime if necessary
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                if key != '__class__' and hasattr(self.__class__, key):
                    setattr(self, key, value)

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.to_dict())

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)

        # Move 'name' to the first position in the dictionary if it exists
        if "name" in new_dict:
            name_value = new_dict.pop("name")
            new_dict = {"name": name_value, **new_dict}

        # Remove SQLAlchemy instance state
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

        return new_dict

    def to_dict_with_class(self):
        """returns a dictionary including the class name"""
        new_dict = self.to_dict()
        new_dict["__class__"] = self.__class__.__name__
        return new_dict

