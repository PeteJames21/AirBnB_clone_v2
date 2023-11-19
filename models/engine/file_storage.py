#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models of specified class from storage"""
        if not cls:
            return self.__objects

        objs = {}
        for k, v in self.__objects.items():
            # `cls` may be a class or the name of a class
            if type(v) is cls or type(v).__name__ == cls:
                objs[k] = v

        return objs

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def delete(self, obj=None):
        """Delete an object from the storage dictionary."""
        if not obj:
            return

        class_name = type(obj).__name__
        try:
            id_ = f"{class_name}.{obj.id}"
            del self.__objects[id_]
        except (KeyError, AttributeError):
            # Do nothing if obj does not exist in the storage dict.
            # AttributeError is raised if object does not have an 'id'.
            # KeyError is raised if no matching id is found in the dict.
            pass

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass
