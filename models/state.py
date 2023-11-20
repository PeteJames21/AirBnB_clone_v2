#!/usr/bin/python3
""" State Module for HBNB project """
from models import storage
from models import City
from models.base_model import BaseModel
from sqlalchemy import Column, String


class State(BaseModel):
    """ State class """
    __tablename__ = "states"

    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="delete")

    if os.getenv("HBNB_TYPE_STORAGE") == "file":
        @property
        def cities(self):
            """Return a list of cities in the current state"""
            lst = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    lst.append(city)
            return lst
