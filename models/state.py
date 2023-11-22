#!/usr/bin/python3
""" State Module for HBNB project """
import os
from sqlalchemy import (Column, String)
from sqlalchemy.orm import relationship
from models.base_model import (BaseModel, Base)


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state',
                          cascade='all, delete, delete-orphan')
    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """Returns the list of `City` class instances attribute
            """
            return self.cities
