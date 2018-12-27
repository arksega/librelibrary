import yaml
from flask import abort

with open('biblio.yaml') as fd:
    raw_data = yaml.load(fd)

data = {}
for book in raw_data:
    if isinstance(book['ISBN'], int):
        isbn = str(book['ISBN'])
    else:
        isbn = book['ISBN'].replace('-', '')
    book['ISBN'] = isbn
    data[isbn] = book


def read():
    return [x for x in data.values()]


def get(isbn):
    if isbn in data:
        return data[isbn]
    else:
        abort(404, 'Book {} not found'.format(isbn))
