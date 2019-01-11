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


def delete(isbn):
    try:
        session.query(orm.Book).filter(orm.Book.isbn == isbn).delete()
        session.commit()
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
    return book, 201


def update(isbn, book):
    book['isbn'] = isbn
    try:
        orm_book = session.query(orm.Book).filter(orm.Book.isbn == isbn).one()
        orm_book.update(book)
        session.commit()
        return '', 204
    except ormexc.NoResultFound:
        orm_book = orm.Book()
        orm_book.update(book)
        session.add(orm_book)
        session.commit()
        return book, 201
    return book
