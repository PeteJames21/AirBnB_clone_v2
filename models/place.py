#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.amenity import Amenity
import os
from models.review import Review
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table

relationship_table = Table(
        "place_amenity", Base.metadata,
        Column("place_id", String(60), ForeignKey("places.id"),
               nullable=False, primary_key=True),
        Column(
            "amenity_id", String(60), ForeignKey("amenities.id"),
            nullable=False, primary_key=True)
        )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship('Review', backref='place', cascade='delete')
    amenities = relationship('Amenity', secondary='place_amenity',
                             viewonly=False)
    amenity_ids = []

    @property
    def reviews(self):
        """Return list of Review instances
        """
        from models import storage
        rev_list = []
        all_revs = storage.all('Review').values()
        for review in all_revs:
            if self.id == review.place_id:
                rev_list.append(review)
        return rev_list

    @property
    def amenities(self):
        """ returns the list of Amenity instances linked to the Place
        """
        from models import storage
        amenity_list = []
        all_amenities = storage.all(Amenity).values()
        for amenity in all_amenities:
            if amenity.id in self.amenity_ids:
                amenity_list.append(amenity)
        return amenity_list

    @amenities.setter
    def amenities(self, obj):
        """Sets method for adding an Amenity.id to the attribute amenity_ids.
        """
        if isinstance(obj, Amenity):
            self.amenity_ids.append(obj.id)
