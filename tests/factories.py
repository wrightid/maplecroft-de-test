import factory
from api.models import User, Site, Area, AreaSite


class UserFactory(factory.Factory):

    username = factory.Sequence(lambda n: "user%d" % n)
    email = factory.Sequence(lambda n: "user%d@mail.com" % n)
    password = "mypwd"

    class Meta:
        model = User

class SiteFactory(factory.Factory):

    id = factory.Sequence(lambda n: "site%d" % n)
    name = factory.Sequence(lambda n: "site%d_name" % n)
    country = "GBR"
    latitude = factory.Sequence(lambda n: "0.%d" % n)
    longitude = factory.Sequence(lambda n: "1.%d" % n)

    class Meta:
        model = Site


class AreaFactory(factory.Factory):

    id = factory.Sequence(lambda n: "area%d" % n)
    shape_name = factory.Sequence(lambda n: "area%d_name" % n)
    shape_group = "GBR"
    shape_type = "ADM3"

    class Meta:
        model = Area
