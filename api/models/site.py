from api.extensions import db

from sqlalchemy import Column, String
# from geoalchemy2 import Geometry


class Site(db.Model):
    """Basic Site model"""
    id = Column(String(128), primary_key=True)
    name = Column(String(128), nullable=False)
    country = Column(String(2), nullable=False)
    # I'd normally use this instead of separate Lat/Lng
    # but keeping separate as relatively complex to install with SQLLite
    # location = Column(Geometry('POINT'), index=True)
    # SQLLite also doesn't support Numeric so need to use a string instead
    latitude = Column(String(20), nullable=False)
    longitude = Column(String(20), nullable=False)
