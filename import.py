import os
import pandas
from sqlalchemy import create_engine, Column, String, Integer,Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

db = create_engine(os.getenv("DATABASE_URL"))
base = declarative_base()

def read_data(address):
    tables = pandas.read_csv(address)
    print(tables.shape[0])
    return tables

class Books(base):
    """docstring for Books."""

    __tablename__ = 'books'

    isbn = Column(String,primary_key = True)
    title = Column(String)
    author = Column(String)
    year = Column(Integer)


class Users(base):
    """docstring fo Users."""
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)





Session = sessionmaker(db)
session = Session()


base.metadata.create_all(db)


def create_books_table(table):
    for i in range(table.shape[0]):

        book = Books(isbn=table['isbn'][i],title = table['title'][i],author= table['author'][i],year=int(table['year'][i]))
        session.add(book)
        session.commit()

def create_users_table(table):
    for i in range(table.shape[0]):


def main():
    create_table()
    print("finished...")


if __name__ == "__main__":
    main()
