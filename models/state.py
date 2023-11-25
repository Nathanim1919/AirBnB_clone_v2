#!/usr/bin/python3
"""
Module Name: models/state.py
Description: State Module definition for HBNB project
"""
import models
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.city import City


class State(BaseModel, Base):
    """State class

    Attributes:
        __tablename__ (table): The name of the table in the database
        name (str): The name of the state
        cities (list): The lsit of cities under the same state
    """
    __tablename__ = 'states'
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state',
                              cascade='all, delete')

    else:
        name = ""

        @property
        def cities(self):
            """Returns the list of `City` class instances attribute
            """
            return [city for city in models.storage.all(City).values()
                    if city.state_id == self.id]
