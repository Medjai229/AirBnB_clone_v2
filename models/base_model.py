#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DataTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DataTime, nullable=False, default=datatime.utcnow())
    updated_at = Column(DataTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            try:
                kwargs['updated_at'] = datetime.strptime(
                        kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
                kwargs['created_at'] = datetime.strptime(
                        kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            except Exception:
                if 'id' not in kwargs.key():
                    self.__init__()
                else:
                    self.created_at = datatime.now()
                    self.updated_at = datatime.now()

            try:
                del kwargs['__class__']
            except Exception:
                pass
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        str_dict = self.__dict__.copy()
        str_dict.pop("_sa_instance_state", None)
        return '[{}] ({}) {}'.format(type(self).__name__, self.id, str_dict)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        """Deletes the current instance from storage"""
        from models import storage
        storage.delete(self)
