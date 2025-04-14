import os
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

from .models import Document, Appendix
from .db_core import Base
import datetime

BASE_DIR = os.path.abspath(os.getcwd())
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

    def add_document(
            self,
            doc_id: str,
            name: str,
            path: str,
            is_income: bool,
            date: datetime.date,
            sender: str = None,
            doc_number: str = None,
            signature_number: str = None,
    ) -> None:
        document = Document(
            id=doc_id,
            doc_name=name,
            is_income=is_income,
            path=path,
            sender=sender,
            date=date,
            doc_number=doc_number,
            signature_number=signature_number
        )
        self._session.add(document)
        self._session.commit()
        self.close()

    def add_appendix(self, doc_id, name, file_path):
        appendix = Appendix(
            document_id=doc_id,
            name=name,
            file_path=file_path,
        )
        self._session.add(appendix)
        self._session.commit()

    def get_doc_by_name(self, doc_name, is_income: bool):
        results = self._session.query(Document).filter_by(
            is_income=is_income,
            doc_name=doc_name,
        ).all()
        self.close()
        return results

    def get_doc_by_date(self, date, is_income: bool):
        results = self._session.query(Document).filter_by(
            is_income=is_income,
            date=date,
        ).all()
        self.close()
        return results

    def get_doc_by_doc_number(self, doc_number: str, is_income: bool):
        results = self._session.query(Document).filter_by(
            is_income=is_income,
            doc_number=doc_number,
        ).all()
        self.close()
        return results

    def get_doc_by_sender(self, sender, is_income):
        results = self._session.query(Document).filter_by(
            is_income=is_income,
            sender=sender
        ).all()
        self.close()
        return results

    def get_document_path(self, name: str, is_income: bool):
        path = self._session.query(Document.path)\
            .filter_by(name=name, is_income=is_income).one()
        self.close()
        return path.path

    def get_appendixes_by_doc_id(self, doc_id: str):
        results = self._session.query(Appendix).filter_by(document_id=doc_id).all()
        self.close()
        return results

