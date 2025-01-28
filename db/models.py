from sqlalchemy import Column, String, Boolean, Integer, Date
from .db_core import Base


class Document(Base):

    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, autoincrement='auto')
    name = Column(String, index=True)
    is_income = Column(Boolean)

    date = Column(Date)

    sender = Column(String)
    inner_number = Column(String, nullable=True)

    path = Column(String, unique=True)

    def __str__(self):
        return f'{self.name}; type={'income' if self.is_income else 'outcome'}'
