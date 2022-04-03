from flask import request, Blueprint
from flask_restful import Api, Resource
from app.common.error_handling import ObjectNotFound

from app.diets.models import Child, Diet

diets_v1_0_bp = Blueprint('diets_v1_0_bp', __name__)

api = Api(diets_v1_0_bp)


class DietListResource(Resource):
    def get(self):
        args = request.args

        child = Child(int(args['age']), float(args['weight']),
                      int(args['height']), int(args['activity']))

        diet = Diet(child)

        # Función que obtiene la dieta filtrada en formato Json
        # dietList = diet.getDiets()

        if dietList is None:
            raise ObjectNotFound('No existen dietas')
        return child.serialize()

api.add_resource(DietListResource, '/api/v1.0/diets',
                 endpoint='diet_list_resource')
