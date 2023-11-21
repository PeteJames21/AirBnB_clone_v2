#!/usr/bin/python3
"""
Create an instance of the storage engine to be used across the entire
application. The type of engine depends on the value of the
HBNB_TYPE_STORAGE environment variable. The storage type defaults to file
storage is this variable is not set.
"""
import os

if os.getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()

else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
