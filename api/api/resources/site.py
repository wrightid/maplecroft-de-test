from flask_jwt_extended import jwt_required
from flask_restful import Resource


class SiteList(Resource):

    method_decorators = [jwt_required()]

    def get(self):
        """ The api should accept a query parameter `?admin_area` and list all the sites
            within this admin area

        :return:
        """
        return {"msg": "Your site list here"}