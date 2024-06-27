#!/usr/bin/python3
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel
from models.user import User
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DBStorage:
    """DBStorage engine"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage engine"""
        user = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        database = os.getenv('HBNB_MYSQL_DB')
        HBNB_ENV = os.getenv('HBNB_ENV')

        self.__engine = create_engine(
                f'mysql+mysqldb://{user}:{password}@{host}/{database}',
                pool_pre_ping=True
        )
        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        result_dict = {}
        if cls:
            query_result = self.__session.query(cls).all()
            for obj in query_result:
                key = f"{obj.__class__.__name__}.{obj.id}"
                result_dict[key] = obj
        else:
            for class_name in BaseModel.__subclasses__():
                query_result = self.__session.query(class_name).all()
                for obj in query_result:
                    key = f"{obj.__class__name__}.{obj.id}"
                    result_dict[key] = obj
        return result_dict

    def new(self, obj):
        """Adds an object to current database session"""
        self.__session.add(obj)

    def save(self):
        """commits all changes to current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """creates all tables"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """Close the current session"""
        self.__session.remove()
