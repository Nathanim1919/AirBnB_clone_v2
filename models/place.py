#!/usr/bin/python3
"""
Module Name: models/place.py
Description: Place Module for HBNB project
"""
import models
import os
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.review import Review
from models.amenity import Amenity

"""Represents the many to many relationship table
between Place and Amenity records.
"""
if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table(
        'place_amenity',
        Base.metadata,
        Column(
            'place_id',
            String(60),
            ForeignKey('places.id'),
            nullable=False,
            primary_key=True
        ),
        Column(
            'amenity_id',
            String(60),
            ForeignKey('amenities.id'),
            nullable=False,
            primary_key=True
        )
    )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(
        String(60), ForeignKey('cities.id'), nullable=False
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    user_id = Column(
        String(60), ForeignKey('users.id'), nullable=False
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    name = Column(
        String(128), nullable=False
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    description = Column(
        String(1024), nullable=True
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    number_rooms = Column(
        Integer, nullable=False, default=0
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    number_bathrooms = Column(
        Integer, nullable=False, default=0
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    max_guest = Column(
        Integer, nullable=False, default=0
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    price_by_night = Column(
        Integer, nullable=False, default=0
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    latitude = Column(
        Float, nullable=True
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else 0.0
    longitude = Column(
        Float, nullable=True
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else 0.0

    reviews = relationship(
        'Review',
        cascade="all, delete, delete-orphan",
        backref='place'
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = relationship(
            'Amenity',
            secondary=place_amenity,
            viewonly=False,
        )

    else:
        amenity_ids = []

        @property
        def amenities(self):
            """Returns the amenities of this Place"""
            amenities_of_place = []
            for value in models.storage.all(Amenity).values():
                if value.id in self.amenity_ids:
                    amenities_of_place.append(value)
            return amenities_of_place

        @amenities.setter
        def amenities(self, value):
            """Adds an amenity to this Place"""
            if type(value) is Amenity:
                if value.id not in self.amenity_ids:
                    self.amenity_ids.append(value.id)

        @property
        def reviews(self):
            """Get a list of `Review` instances with `place_id` equals
            to the current `place.id`
            """
            return [review for review in models.storage.all(Review).values()
                    if review.place_id == self.id]
