import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Singleton(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs, **kwargs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)

        return cls._instance
