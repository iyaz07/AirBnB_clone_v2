#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return FileStorage.__objects
        else:
            obj_dict = {}
            for key, value in FileStorage.__objects.items():
                if isinstance(value, cls):
                    obj_dict[key] = value
            return obj_dict

    def new(self, obj):
        """Adds new object to storage dictionary"""
        if obj.__class__.__name__ not in self.__objects:
            self.__objects[obj.to_dict()['__class__'] + '.' + obj.id] = obj
    def save(self):
        """Saves storage dictionary to file"""
        with open(self.__file_path, 'w') as f:
            temp = {key: obj.to_dict() for key, obj in self.__objects.items()}
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            with open(self.__file_path, 'r') as f:
                data = json.load(f)
                for key, val in data.items():
                    cls_name = val['__class__']
                    if cls_name in classes:
                        self.__objects[key] = classes[cls_name](**val)
        except FileNotFoundError:
            pass
        except JSONDecodeError:
            print("Error decoding JSON")

    def delete(self, obj=None):
        """Delects obj from __objects"""
        if obj is not None:
            if obj in FileStorage.__objects.values():
                key = "{}.{}".format(obj.to_dict()['__class__'], obj.id)
                del (FileStorage.__objects[key])

    def close(self):
        """close"""
        self.reload()
