from flask_jwt_extended import jwt_required
from flask_restful import Resource


class SiteList(Resource):

    method_decorators = [jwt_required()]

    def get(self):
        return {"msg": "Your site list here"}