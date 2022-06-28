from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import column_property, relationship
from sqlalchemy.sql.functions import Function

from engine import engine

Base = declarative_base()

class VeryAbstractThing(object):
    foo = Column("foo", Integer, nullable=False)
    bar = Column("bar", Integer, nullable=True)

    @declared_attr
    def foobar(self):
        return column_property(Function("least", self.foo, self.bar, type_=Integer), deferred=True)

class AbstractThing(VeryAbstractThing, Base):
    __abstract__ = True

    baz = Column("baz", Integer, nullable=True)

    @declared_attr
    def foobarbaz(self):
        return column_property(Function("least", self.foo, self.bar, self.baz, type_=Integer), deferred=True)

class RealThing(AbstractThing):
    __tablename__ = "real_things"

    id = Column(Integer, primary_key=True)

class RealThingChild(AbstractThing):
    __tablename__ = "real_thing_children"

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("real_things.id"))
    parent = relationship("RealThing", backref="children")


Base.metadata.create_all(engine)
