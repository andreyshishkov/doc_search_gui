import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Document
from .db_core import Base

BASE_DIR = os.path.abspath(os.getcwd())
print(BASE_DIR)
DATABASE = os.path.join('sqlite:///' + BASE_DIR, 'documents.db')


class Singleton(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs, **kwargs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)

        return cls._instance


class DBManager(metaclass=Singleton):

    def __init__(self):
        self.engine = create_engine(DATABASE)
        session = sessionmaker(bind=self.engine)
        self._session = session()
        if not os.path.isfile(DATABASE):
            Base.metadata.create_all(self.engine)

    def close(self):
        self._session.close()

    def rollback(self):
        self._session.rollback()

    def add_document(self, name: str, path: str, is_income: bool) -> None:
        document = Document(
            name=name,
            is_income=is_income,
            path=path,
        )
        self._session.add(document)
        self._session.commit()
        self.close()

    def get_document_path(self, name: str, is_income: bool):
        path = self._session.query(Document.path)\
            .filter_by(name=name, is_income=is_income).one()
        self.close()
        return path.path
