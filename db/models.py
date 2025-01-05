from sqlalchemy import Column, String, Boolean
from .db_core import Base


class Document(Base):

    __tablename__ = 'documents'
    name = Column(String, index=True, primary_key=True)
    is_income = Column(Boolean)
    path = Column(String, unique=True)

    def __str__(self):
        return f'{self.name}; type={'income' if self.is_income else 'outcome'}'
