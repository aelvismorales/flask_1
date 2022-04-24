from flask import request, Blueprint, url_for
from flask_restful import Api, Resource
from app.common.error_handling import ObjectNotFound

import warnings
import pandas as pd
from pandas.core.common import SettingWithCopyWarning

from app.diets.models import Child, Diet

warnings.simplefilter(action='ignore', category=SettingWithCopyWarning)

diets_v1_0_bp = Blueprint('diets_v1_0_bp', __name__, url_prefix='/')

data = []


@diets_v1_0_bp.before_app_first_request
def getData():
    url = 'https://raw.githubusercontent.com/aelvismorales/flask_1/main/dataset.csv'
    global data
    data = pd.read_csv(url, encoding='utf8')

api = Api(diets_v1_0_bp)


class DietListResource(Resource):
    def post(self):
        args = request.get_json()

        keys = ['age', 'weight', 'height', 'activity', 'sex', 'days',
                'preference']

        for key in keys:
            if key not in args.keys():
                raise ObjectNotFound('Falta un campo en la petición')

        age = args[keys[0]]
        weight = args[keys[1]]
        height = args[keys[2]]
        activity = args[keys[3]]
        sex = args[keys[4]]
        days = args[keys[5]]
        preference = args[keys[6]]
   
        child = Child(age, weight, height, activity, sex, preference)
 

        diet = Diet(child, data)

        dietList = None
        dietList = diet.getDiets(days)

        if dietList is None:
            raise ObjectNotFound('No existen dietas')

        return dietList

class recomendation(Resource):
    def post(self):
        args=request.get_json()

        keys=['type','calories']
        for key in keys:
            if key not in args.keys():
                raise ObjectNotFound('Falta un campo en la petición')
        type=args[keys[0]]
        calories=args[keys[1]]

        child=Child(type,calories)
        diet = Diet(child, data)

        dietList=None
        dietList=diet.get3foods()

        if dietList is None:
            raise ObjectNotFound('No existen dietas')

        return dietList


api.add_resource(DietListResource, '/api/v1.0/diets',
                 endpoint='diet_list_resource')

api.add_resource(recomendation, '/api/v1.0/refoods',
                 endpoint='recomendation')

