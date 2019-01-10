import sqlalchemy.orm.exc as ormexc
from sqlalchemy import exc as pyormexc
from flask import abort
import orm

session = orm.init()


def read():
    return [dict(item) for item in session.query(orm.Book).all()]


def get(isbn):
    try:
        r = session.query(orm.Book).filter(orm.Book.isbn == isbn).one()
        return dict(r)
    except ormexc.NoResultFound:
        abort(404, 'Book {} not found'.format(isbn))


def create(book):
    orm_book = orm.Book()
    try:
        orm_book.update(book)
        session.add(orm_book)
        session.commit()
    except pyormexc.IntegrityError:
        session.rollback()
        abort(409, 'ISBN {} already exist'.format(orm_book.isbn))
    return dict(orm_book)
