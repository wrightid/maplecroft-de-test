from flask import request

from flask_jwt_extended import jwt_required
from flask_restful import Resource

from api.api.schemas import SiteSchema

from api.models import Site
from api.commons.pagination import paginate


class SiteList(Resource):

    method_decorators = [jwt_required()]

    def get(self):
        """Get all sites in an area

        The api should accept a query parameter `?admin_area` and list all the sites
            within this admin area
    ---
    get:
      tags:
        - api
       parameters:
        - in: request
          name: admin_area
          schema:
            type: string
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/SiteSchema'

        """

        admin_area = None
        if 'admin_area' in request.args:
            admin_area = request.args["admin_area"]

        print(admin_area)

        schema = SiteSchema(many=True)
        query = Site.query
        return paginate(query, schema)
