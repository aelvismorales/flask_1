import pandas as pd
import json
import numpy as np

def quantity_food_g(x):
  return 100*x['Multiplicador_Cantidad_Comer']

def requierement_ok(x):
  if x['Multiplicador_Cantidad_Comer'] >=1 and x['Multiplicador_Cantidad_Comer']<=11:
    return True
  else:
    return False


class Child:

    def __init__(self, age, weight, height, activity, sex):
        self.age = age
        self.weight = weight
        self.height = height
        self.activity = activity
        self.sex = sex
        self.TMB=self.get_TMB()

    # Función que calcula las macros del niño
    def get_TMB(self):
        if self.sex=='F':
            if self.activity=='Sedentario':
                TMB=(655.0955 + (9.5634 * self.weight) + (1.8449 * self.height) - (4.6756 *self.age))*1.20
                return TMB
            elif self.activity=='Baja_Actividad':
                TMB=(655.0955 + (9.5634 * self.weight) + (1.8449 * self.height) - (4.6756 *self.age))*1.375
                return TMB
            elif self.activity=='Activo':
                TMB=(655.0955 + (9.5634 * self.weight) + (1.8449 * self.height) - (4.6756 *self.age))*1.725
                return TMB
            elif self.activity=='Muy_Activo':
                TMB=(655.0955 + (9.5634 * self.weight) + (1.8449 * self.height) - (4.6756 *self.age))*1.90
                return TMB
            else :
              return None
        else :
            if self.activity=='Sedentario':
                TMB=(66.4730 + (13.7516 * self.weight) + (5.0033 * self.height) - (6.7550 *self.age))*1.20
                return TMB
            elif self.activity=='Baja_Actividad':
                TMB=(66.4730 + (13.7516 * self.weight) + (5.0033 * self.height) - (6.7550 *self.age))*1.375
                return TMB
            elif self.activity=='Activo':
                TMB=(66.4730 + (13.7516 * self.weight) + (5.0033 * self.height) - (6.7550 *self.age))*1.725
                return TMB
            elif self.activity=='Muy_Activo':
                TMB=(66.4730 + (13.7516 * self.weight) + (5.0033 * self.height) - (6.7550 *self.age))*1.90
                return TMB
            else:
              return None

    def get_cal_d(self): #Carbohidratos
      return ((self.TMB)*0.6)*0.3
    def get_cal_a(self):
      return ((self.TMB)*0.6)*0.4

    def get_g_d(self):#grasas
      return ((self.TMB)*0.3)*0.3
    def get_g_a(self):
      return ((self.TMB)*0.3)*0.4

    def get_p_d(self):#proteinas
      return ((self.TMB)*0.10)*0.3
    def get_p_a(self):
      return ((self.TMB)*0.10)*0.4

    def serialize(self):
        return {
                'age': self.age,
                'weight': self.weight,
                'height': self.height,
                'activity': self.activity,
                'sex': self.sex
                }


class Diet:
    def __init__(self, child, data):
        self.child = child
        self.data = data
        #print(self.child.get_p_a)

    # Agregar aquí las funciones para filtrar la dieta y devolver
    # La lista filtrada en formato Json
    def get_desayuno(self):
      dt_desayuno=self.data[(self.data['Horario_1']=='Desayuno')|(self.data['Horario_2']=='Desayuno')]
      dt_desayuno['Total_Calorias_Desayuno']=self.child.get_cal_d()+self.child.get_g_d()+self.child.get_p_d()

      dt_desayuno['Multiplicador_Cantidad_Comer']=(dt_desayuno['Total_Calorias_Desayuno']/dt_desayuno['Calorias_Total_100g'])
      dt_desayuno['Cumple_Requisitos']=dt_desayuno.apply(requierement_ok,axis=1)
      dt_desayuno=dt_desayuno[(dt_desayuno['Cumple_Requisitos']==True)]
      dt_desayuno['Cantidad_Gramos_Consumir']=dt_desayuno.apply(quantity_food_g,axis=1)
      #print(dt_desayuno[['Alimento','Proteinas','Grasas','Carbohidratos','Cantidad_Gramos_Consumir']].to_json(orient='records'))
      return dt_desayuno[['Alimento','Proteinas','Grasas','Carbohidratos','Cantidad_Gramos_Consumir']] 

    #def get_desayuno(self):
    #    dt_desayuno = self.data[(self.data['Horario_1']=='Desayuno')|(self.data['Horario_2']=='Desayuno')]
    #    dt_desayuno['Multiplicador_Calorias']=(self.child.get_cal_d()/dt_desayuno['Calorias_Total_100g'])
    #    dt_desayuno['Multiplicador_Proteinas']=(self.child.get_p_d()/dt_desayuno['Proteinas'])
    #    dt_desayuno=dt_desayuno.assign(Cumple_Requisitos=lambda x: pd.cut(abs(x['Multiplicador_Calorias']-x['Multiplicador_Proteinas']),bins=[0,1,2],labels=[True,False]))
    #    dt_desayuno=dt_desayuno.assign(Diferencia=lambda x: (abs(x['Multiplicador_Calorias']-x['Multiplicador_Proteinas'])))
    #    dt_desayuno=dt_desayuno[(dt_desayuno['Cumple_Requisitos']==True) & (dt_desayuno['Diferencia']<=1)]
    #    dt_desayuno['Total_Comer']=dt_desayuno.apply(total_comer,axis=1)
        
        #return dt_desayuno[['Alimento','Total_Comer']]

    def get_almuerzo(self):
      dt_almuerzo=self.data[(self.data['Horario_1']=='Almuerzo')|(self.data['Horario_2']=='Almuerzo')]
      dt_almuerzo['Total_Calorias_Almuerzo']=self.child.get_cal_a()+self.child.get_g_a()+self.child.get_p_a()
      dt_almuerzo['Multiplicador_Cantidad_Comer']=(dt_almuerzo['Total_Calorias_Almuerzo']/dt_almuerzo['Calorias_Total_100g'])
      dt_almuerzo['Cumple_Requisitos']=dt_almuerzo.apply(requierement_ok,axis=1)
      dt_almuerzo=dt_almuerzo[(dt_almuerzo['Cumple_Requisitos']==True)]
      dt_almuerzo['Cantidad_Gramos_Consumir']=dt_almuerzo.apply(quantity_food_g,axis=1)
      return dt_almuerzo[['Alimento','Proteinas','Grasas','Carbohidratos','Cantidad_Gramos_Consumir']]


    #def a_recomendado(self):
    #    dt_almuerzo=self.data[(self.data['Horario_1']=='Almuerzo')|(self.data['Horario_2']=='Almuerzo')]
    #    dt_almuerzo['Multiplicador_Calorias']=(self.child.get_cal_a()/dt_almuerzo['Calorias_Total_100g'])
    #    dt_almuerzo['Multiplicador_Proteinas']=(self.child.get_p_a()/dt_almuerzo['Proteinas'])
    #    dt_almuerzo=dt_almuerzo.assign(Cumple_Requisitos=lambda x: pd.cut(abs(x['Multiplicador_Calorias']-x['Multiplicador_Proteinas']),bins=[0,1,2],labels=[True,False]))
    #    dt_almuerzo=dt_almuerzo.assign(Diferencia=lambda x: (abs(x['Multiplicador_Calorias']-x['Multiplicador_Proteinas'])))
    #    dt_almuerzo=dt_almuerzo[(dt_almuerzo['Cumple_Requisitos']==True) & (dt_almuerzo['Diferencia']<=1)]
    #    dt_almuerzo['Total_Comer']=dt_almuerzo.apply(total_comer,axis=1)
#
    #    return dt_almuerzo[['Alimento','Total_Comer']]
    def get_cena(self):
      dt_cena=self.data[(self.data['Horario_1']=='Almuerzo')|(self.data['Horario_2']=='Almuerzo')]
      dt_cena['Total_Calorias_Cena']=self.child.get_cal_d()+self.child.get_g_d()+self.child.get_p_d()
      dt_cena['Multiplicador_Cantidad_Comer']=(dt_cena['Total_Calorias_Cena']/dt_cena['Calorias_Total_100g'])
      dt_cena['Cumple_Requisitos']=dt_cena.apply(requierement_ok,axis=1)
      dt_cena['Cantidad_Gramos_Consumir']=dt_cena.apply(quantity_food_g,axis=1)
      return dt_cena[['Alimento','Proteinas','Grasas','Carbohidratos','Cantidad_Gramos_Consumir']]
    #def c_recomendado(self):
    #  dt_cena=self.data[(self.data['Horario_1']=='Cena')|(self.data['Horario_2']=='Cena')]
    #  dt_cena['Multiplicador_Calorias']=(self.child.get_cal_c()/dt_cena['Calorias_Total_100g'])
    #  dt_cena['Multiplicador_Proteinas']=(self.child.get_p_c()/dt_cena['Proteinas'])
    #  dt_cena=dt_cena.assign(Cumple_Requisitos=lambda x: pd.cut(abs(x['Multiplicador_Calorias']-x['Multiplicador_Proteinas']),bins=[0,1,2],labels=[True,False]))
    #  dt_cena=dt_cena.assign(Diferencia=lambda x: (abs(x['Multiplicador_Calorias']-x['Multiplicador_Proteinas'])))
    #  dt_cena=dt_cena[(dt_cena['Cumple_Requisitos']==True) & (dt_cena['Diferencia']<=1)]
    #  dt_cena['Total_Comer']=dt_cena.apply(total_comer,axis=1)
#
#      return dt_cena[['Alimento','Total_Comer']]
#

    def getDiets(self):
        result_desayuno = self.get_desayuno()
        result_desayuno['Tipo']='desayuno'

        result_almuerzo=self.get_almuerzo()
        result_almuerzo['Tipo']='almuerzo'

        result_cena=self.get_cena()
        result_cena['Tipo']='cena'

        dieta=pd.concat([result_desayuno.sample(n=15),result_almuerzo.sample(n=15),result_cena.sample(n=15)],ignore_index=True)

        result =dieta.to_json(orient='split')
        #parsed = json.loads(result)
        #return json.dumps(parsed, indent=4)
        return result
