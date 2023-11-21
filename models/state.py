#!/usr/bin/python3
""" State Module for HBNB project """
import models
import os
from .city import City
from .base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="delete")

    if os.getenv("HBNB_TYPE_STORAGE") == "file":
        @property
        def cities(self):
            """Return a list of cities in the current state"""
            lst = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    lst.append(city)
            return lst
