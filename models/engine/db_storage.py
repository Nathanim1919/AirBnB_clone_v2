#!/usr/bin/python3
"""
Module Name: models/engine/db_storage.py
Description: A definition of mysql database for the models
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """A definition of `DBStorage` class for database connection,
       and management for the models

    Attributes:
        __engine (sqlalchemy): The engine for connection to the database
        __session (sqlalchemy): The session to be used to interact with the
                                database
    """
    __engine = None
    __session = None

    def __init__(self):
        """Instantiates the database attributes
        """

        """ Environment variables """
        USER = os.getenv('HBNB_MYSQL_USER')
        PWD = os.getenv('HBNB_MYSQL_PWD')
        HOST = os.getenv('HBNB_MYSQL_HOST')
        DB = os.getenv('HBNB_MYSQL_DB')

        url = 'mysql+mysqldb://{}:{}@{}/{}'.format(
            USER, PWD, HOST, DB)
        self.__engine = create_engine(url, pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries the database for all objects of class name `cls`
        if not none, otherwise map all objects
        """
        classes = [State, City, User, Place, Review, Amenity]
        objs = []
        if cls:
            objs = self.__session.query(cls).all()
        else:
            for class_name in classes:
                objs.extend(self.__session.query(class_name).all())

        obj_dict = {}
        for obj in objs:
            key = f"{obj.__class__.__name__}.{obj.id}"
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
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database
        """
        # Create all tables
        Base.metadata.create_all(self.__engine)

        # Create current database session
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ call close on private session. """
        self.__session.close()
