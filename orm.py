from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

Base = declarative_base()


class SQLAlchemyDict(object):
    def __getitem__(self, key):
        return getattr(self, key)

    def __iter__(self):
        return ((i.name, getattr(self, i.name)) for i in self.__table__.columns)

    def __len__(self):
        return len(self.__table__.columns)

    def keys(self):
        return (x for x, y in iter(self))

    def update(self, other):
        valid = set(self.keys())
        for k, v in other.items():
            assert k in valid
            setattr(self, k, v)


class Book(Base, SQLAlchemyDict):
    __tablename__ = 'book'
    author = Column(String)
    editorial = Column(String)
    title = Column(String)
    year = Column(String)
    isbn = Column(String, primary_key=True)


def init(constr=None):
    if not constr:
        # constr = 'postgresql://library:1234@localhost/library'
        # constr = 'sqlite:///library.db'
        constr = 'sqlite:///:memory:'
    engine = create_engine(constr)
    session_factory = sessionmaker(bind=engine)
    session = scoped_session(session_factory)
    Base.metadata.create_all(engine)
    return session
