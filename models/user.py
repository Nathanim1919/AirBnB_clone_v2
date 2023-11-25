#!/usr/bin/python3
"""
Module Name: models/user.py
Description: This module defines a class User
"""
import os
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """This class defines a user by various attributes

    This class also defines some attributes relationship to use database

    Attributes:
        __tablename__ (table): The name of the table in the database
        email (str): Email of the user instance
        password (str): Password
        first_name (str): User first name
        last_name (str): User last name
        places (list): The list of attributes in relation to `Place` class
        review (list): The list of attributes in relation to `Review` class
    """
    __tablename__ = 'users'

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=False)
        places = relationship('Place', backref='user',
                              cascade='all, delete')
        reviews = relationship('Review', backref='user',
                               cascade='all, delete')
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
