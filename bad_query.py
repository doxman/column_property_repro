from sqlalchemy.orm import sessionmaker

from engine import engine
from models import RealThing, RealThingChild

Session = sessionmaker(bind=engine)

session = Session()

query = session.query(RealThingChild).join(
    RealThing,
    RealThingChild.parent_id == RealThing.id
).filter(RealThingChild.foobarbaz < 3)

query.count()  # This will fail with ambiguous column
