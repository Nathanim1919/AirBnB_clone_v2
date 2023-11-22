#!/usr/bin/python3
"""
Module Name: models/place.py
Description: Place Module for HBNB project
"""
import models
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    reviews = relationship('Review', backref='place',
                           cascade='all, delete, delete-orphan')

    @property
    def reviews(self):
        """Get a list of `Review` instances with `place_id` equals
        to the current `place.id`
        """
        return [review for reviews in models.storage.all().values()
                if reviews.place_id == self.id]
