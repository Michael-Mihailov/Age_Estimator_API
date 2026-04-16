from db.engine import engine, SessionLocal
from db.base import Base
from db.models import NameStats

Base.metadata.create_all(engine) # creates the tables in the database if they don't exist yet
session = SessionLocal()

# TODO: add code here

session.close()