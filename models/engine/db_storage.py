#!/usr/bin/python3
"""
Module Name: models/engine/db_storage.py
Description: A definition of mysql database for the models
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import (sessionmaker, scoped_session)
from models.base_model import Base


class DBStorage:
    """A definition of `DBStorage` class for database connection,
    and management for the models
    """
    __engine = None
    __session = None

    def __init__(self):
        """Instantiates the database attributes
        """

        """ Environment variables """
        HBNB_MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = 'localhost'
        HBNB_MYSQL_DB = os.getenv('HBNB_MYSQL_DB')

        url = 'mysql+mysqldb://{}:{}@localhost/{}'.format(
            HBNB_MYSQL_USER, HBNB_MYSQL_PWD, HBNB_MYSQL_DB)
        self.__engine = create_engine(url, pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries the database for all objects of class name `cls`
        if not none, otherwise map all objects
        """
        obj_dict = {}
        session_objects = self.__session.identity_map.values()
        if cls:
            for obj in session_objects:
                if type(obj).__name__ == eval(cls):
                    key = "cls.{}".format(obj.id)
                    obj_dict[key] = obj
        else:
            for obj in session_objects:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[key] = obj

        return obj_dict

    def new(self, obj):
        """Add an object to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Delete the given `obj` from the current database session
        """
        if obj:
            self.__session.query(obj).delete()

    def reload(self):
        """Create all tables in the database
        """
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        # Create all tables
        Base.metadata.create_all(self.__engine)

        # Create current database session
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
