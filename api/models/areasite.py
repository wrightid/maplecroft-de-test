"""Represent the relationship between sites and areas
"""
from api.extensions import db


class AreaSite(db.Model):
    """AreaSite representation"""

    site_id = db.Column(db.String(128), db.ForeignKey("site.id"), primary_key=True)
    area_id = db.Column(db.String(128), db.ForeignKey("area.id"), primary_key=True)

    site = db.relationship("Site", lazy="joined")
    area = db.relationship("Area", lazy="joined")

    def __repr__(self):
        return f"""<AreaSite Site ID {self.site_id}
    Area ID {self.area_id}
    >"""
