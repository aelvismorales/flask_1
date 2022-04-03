import pandas as pd

#data=pd.read_csv('app\diets\dataset.csv')
def total_comer(x):
  if x['Diferencia']>=0.4 and x['Diferencia']<=1:
    return (x['Multiplicador_Proteinas']*x['Calorias_Total_100g'])*(1+(1-x['Diferencia']))
  else:
    return x['Multiplicador_Proteinas']*x['Calorias_Total_100g']

class Child:
    def __init__(self, age, weight, height, activity,sex):
        self.age = age
        self.weight = weight
        self.height = height
        self.activity = activity
        self.sex=sex

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
            else:
                TMB=(655.0955 + (9.5634 * self.weight) + (1.8449 * self.height) - (4.6756 *self.age))*1.90
                return TMB
        else:
            if self.activity=='Sedentario':
                TMB=(66.4730 + (13.7516 * self.weight) + (5.0033 * self.height) - (6.7550 *self.age))*1.20
                return TMB
            elif self.activity=='Baja_Actividad':
                TMB=(66.4730 + (13.7516 * self.weight) + (5.0033 * self.height) - (6.7550 *self.age))*1.375
                return TMB
            elif self.activity=='Activo':
                TMB=(66.4730 + (13.7516 * self.weight) + (5.0033 * self.height) - (6.7550 *self.age))*1.725
                return TMB
            else :
                TMB=(66.4730 + (13.7516 * self.weight) + (5.0033 * self.height) - (6.7550 *self.age))*1.90
                return TMB
    def get_cal_d(self):
      return self.get_TMB()*0.3
    def get_cal_a(self):
      return self.get_TMB()*0.4
    def get_cal_c(self):
      return self.get_TMB()*0.3

    def get_p_d(self):
      return (self.weight*0.84)*0.3
    def get_p_d(self):
      return (self.weight*0.84)*0.4
    def get_p_c(self):
      return (self.weight*0.84)*0.3
        

    def serialize(self):
        return {
                'age': self.age,
                'weight': self.weight,
                'height': self.height,
                'activity': self.activity,
                'sex':self.sex
                }


class Diet:
    def __init__(self, child,data):
        self.child = child
        self.data=data

    # Agregar aquí las funciones para filtrar la dieta y devolver
    # La lista filtrada en formato Json
    def get_desayuno(self):
      dt_desayuno=self.data[(self.data['Horario_1']=='Desayuno')|(self.data['Horario_2']=='Desayuno')]
      dt_desayuno['Multiplicador_Calorias']=(self.child.get_cal_d()/dt_desayuno['Calorias_Total_100g'])
      dt_desayuno['Multiplicador_Proteinas']=(self.child.get_p_d()/dt_desayuno['Proteinas'])
      dt_desayuno=dt_desayuno.assign(Cumple_Requisitos=lambda x: pd.cut(abs(x['Multiplicador_Calorias']-x['Multiplicador_Proteinas']),bins=[0,1,2],labels=[True,False]))
      dt_desayuno=dt_desayuno.assign(Diferencia=lambda x: (abs(x['Multiplicador_Calorias']-x['Multiplicador_Proteinas'])))
      dt_desayuno=dt_desayuno[(dt_desayuno['Cumple_Requisitos']==True) & (dt_desayuno['Diferencia']<=1)]
      dt_desayuno['Total_Comer']=dt_desayuno.apply(total_comer,axis=1)
      return dt_desayuno[['Alimento','Total_Comer']]

    def a_recomendado(self):
      dt_almuerzo=self.data[(self.data['Horario_1']=='Almuerzo')|(self.data['Horario_2']=='Almuerzo')]
      dt_almuerzo['Multiplicador_Calorias']=(self.child.get_cal_a()/dt_almuerzo['Calorias_Total_100g'])
      dt_almuerzo['Multiplicador_Proteinas']=(self.child.get_p_a()/dt_almuerzo['Proteinas'])
      dt_almuerzo=dt_almuerzo.assign(Cumple_Requisitos=lambda x: pd.cut(abs(x['Multiplicador_Calorias']-x['Multiplicador_Proteinas']),bins=[0,1,2],labels=[True,False]))
      dt_almuerzo=dt_almuerzo.assign(Diferencia=lambda x: (abs(x['Multiplicador_Calorias']-x['Multiplicador_Proteinas'])))
      dt_almuerzo=dt_almuerzo[(dt_almuerzo['Cumple_Requisitos']==True) & (dt_almuerzo['Diferencia']<=1)]
      dt_almuerzo['Total_Comer']=dt_almuerzo.apply(total_comer,axis=1)
      return dt_almuerzo[['Alimento','Total_Comer']]

    def c_recomendado(self):
      dt_cena=self.data[(self.data['Horario_1']=='Cena')|(self.data['Horario_2']=='Cena')]
      dt_cena['Multiplicador_Calorias']=(self.child.get_cal_c()/dt_cena['Calorias_Total_100g'])
      dt_cena['Multiplicador_Proteinas']=(self.child.get_p_c()/dt_cena['Proteinas'])
      dt_cena=dt_cena.assign(Cumple_Requisitos=lambda x: pd.cut(abs(x['Multiplicador_Calorias']-x['Multiplicador_Proteinas']),bins=[0,1,2],labels=[True,False]))
      dt_cena=dt_cena.assign(Diferencia=lambda x: (abs(x['Multiplicador_Calorias']-x['Multiplicador_Proteinas'])))
      dt_cena=dt_cena[(dt_cena['Cumple_Requisitos']==True) & (dt_cena['Diferencia']<=1)]
      dt_cena['Total_Comer']=dt_cena.apply(total_comer,axis=1)
      return dt_cena[['Alimento','Total_Comer']]
