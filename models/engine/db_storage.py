#!/usr/bin/python3
"""database storage engine"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """Defines DB storage class"""
    __engine = None
    __session = None

    def __init__(self):
        """initilazes DBstorage Class"""
        hbnb_dev_user = getenv('HBNB_MYSQL_USER')
        hbnb_dev_pwd = getenv('HBNB_MYSQL_PWD')
        hbnb_dev_host = getenv('HBNB_MYSQL_HOST')
        hbnb_dev_db = getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(hbnb_dev_user,
                                              hbnb_dev_pwd,
                                              hbnb_dev_host,
                                              hbnb_dev_db
                                              ), pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """query on the current database session (self.__session) all objects
        depending of the class name (argument cls)"""
        objs_dict = {}
        if cls is None:
            tables_list = [State, City, User, Place]

        else:
            if isinstance(cls, str):
                cls = eval(cls)

            tables_list = [cls]

        for table in tables_list:
            objects = self.__session.query(table).all()

            for item in objects:
                key = "{}.{}".format(item.__class__.__name__, item.id)
                objs_dict[key] = item

        return objs_dict

    def new(self, obj):
        """add the object to the current
        database session (self.__session)"""

        self.__session.add(obj)

    def save(self):
        '''commit all changes of the current db session'''
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the database"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """"""
        Base.metadata.create_all(self.__engine)
        Session_maker = sessionmaker(bind=self.__engine,
                                     expire_on_commit=False)
        session = scoped_session(Session_maker)
        self.__session = session()

    def close(self):
        """closes the working SQLAlchemy session"""
        self.__session.close()
