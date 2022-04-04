from flask import request, Blueprint, url_for
from flask_restful import Api, Resource
from app.common.error_handling import ObjectNotFound
import pandas as pd
import json

from app.diets.models import Child, Diet

diets_v1_0_bp = Blueprint('diets_v1_0_bp', __name__, url_prefix ='/')

data = []


@diets_v1_0_bp.before_app_first_request
def getData():
    url='https://raw.githubusercontent.com/aelvismorales/flask_1/main/dataset.csv'
    #url = 'https://raw.githubusercontent.com/TDP-2022-01/dieta-api/dev/app/diets/dataset.csv'
    global data
    data = pd.read_csv(url)
    #print(data.head())

api = Api(diets_v1_0_bp)


class DietListResource(Resource):
    def get(self):
        args = request.args

        child = Child(int(args['age']), float(args['weight']),
                      int(args['height']), args['activity'], args['sex'])
        diet = Diet(child, data)

        # Función que obtiene la dieta filtrada en formato Json
        dietList = []
        #print(diet)
        dietList = diet.getDiets()
        #print(dietList)
        if dietList is None:
            raise ObjectNotFound('No existen dietas')
        return dietList

api.add_resource(DietListResource, '/api/v1.0/diets',
                 endpoint='diet_list_resource')