from sqlalchemy.engine import create_engine

engine = create_engine(
    "postgresql://column_property_repro:password@localhost/column_property_repro",
)
