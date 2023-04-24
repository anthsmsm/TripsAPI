from sqlalchemy import Column, Integer, String, DateTime
from geoalchemy2.types import Geometry
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

"""
Class used by SQLAlchemy to represent the table Trips in the database.
"""
class TripEntity(Base):
    __tablename__ = 'trips'
    id = Column(Integer, primary_key=True)
    region = Column(String)
    origin_coord = Column(Geometry('POINT'))
    destination_coord = Column(Geometry('POINT'))
    datetime = Column(DateTime)
    datasource = Column(String)
    trip_group = Column(String)
