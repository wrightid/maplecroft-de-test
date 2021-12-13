from sqlalchemy import Column

from sqlalchemy import String
from api.extensions import db


class Area(db.Model):
    """Area representation"""

    id = Column(String(128), primary_key=True)
    shape_name = Column(String(128), nullable=True)
    shape_group = Column(String(32), nullable=False)
    shape_type = Column(String(32), nullable=False)

    def __repr__(self):
        return f"""<Area ID {self.id}
    {self.shape_name}
    {self.shape_group}
    {self.shape_type}
    >"""
