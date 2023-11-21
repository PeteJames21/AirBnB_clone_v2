#!/usr/bin/python3
"""
Defines a class for managing MySQL database storage.
"""

import os
from sqlalchemy import create_engine
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.review import Review
from models.amenity import Amenity
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


class DBStorage:
    """A class for managing MySQL data storage."""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize an instance of this class."""
        URL = "mysql+mysqldb://{}:{}@{}:3306/{}".format(
                os.getenv("HBNB_MYSQL_USER"),
                os.getenv("HBNB_MYSQL_PWD"),
                os.getenv("HBNB_MYSQL_HOST"),
                os.getenv("HBNB_MYSQL_DB"))
        self.__engine = create_engine(URL, pool_pre_ping=True)

        # Drop all tables in we are in the test environment
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Return a dictionary of models of specified class from storage."""
        classes = [State, City, User, Place, Review, Amenity]
        objects_list = []
        if not cls:
            # Get objects from all tables
            for cls in classes:
                objects_list += self.__session.query(cls).all()
        else:
            # Get objects from the specified table
            objects_list = self.__session.query(cls).all()

        # Pack the objects into a dictionary.
        objects_dict = {}
        for obj in objects_list:
            id_ = f"{type(obj).__name__}.{obj.id}"
            objects_dict[id_] = obj

        return objects_dict

    def new(self, obj):
        """Add an object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all pending changes in the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current database session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create a new session."""
        # Create tables whose mapped classes have been imported in this module
        Base.metadata.create_all(self.__engine)
        # Initialize a thread-safe session
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
