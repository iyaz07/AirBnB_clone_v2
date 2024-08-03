import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review

class DBStorage:
    """DBStorage engine"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage engine"""
        user = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')
        
        DATABASE_URL = f"mysql+mysqldb://{user}:{password}@{host}:3306/{database}"

        self.__engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of all objects, optionally filtered by class"""
        objects = {}

        if cls is None:
            all_classes = [User, State, City, Amenity, Place, Review]
            for class_type in all_classes:
                query = self.__session.query(class_type)
                for obj in query.all():
                    obj_key = f"{obj.__class__.__name__}.{obj.id}"
                    objects[obj_key] = obj
        else:
            query = self.__session.query(cls)
            for obj in query.all():
                obj_key = f"{obj.__class__.__name__}.{obj.id}"
                objects[obj_key] = obj

        return objects

    def new(self, obj):
        """Adds an object to the current database session"""
        if obj is not None:
            self.__session.add(obj)

    def save(self):
        """Commits all changes to the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables and initializes a new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """Closes the current session"""
        self.__session.close()

