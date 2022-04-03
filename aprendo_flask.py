from flask import Flask,render_template
from flask import request

app=Flask(__name__) # Nuevo objeto
# A que ruta el cliente debe acceder - wrap (decorador)
@app.route('/')
def index():
    return 'Hola Mundo'

@app.route('/saluda')
def saludo():
    
    #name_saludo=request.args.get('saludo1','no se encontro un nombre')
    return render_template('init.html')
if __name__=='__main__':
    app.run(debug=True,port=8000) #Se encarga de ejecutar el servidor por default el 5000 - Si agregamos como variable input port podemos cambiar el puerto de uso
#Si ponemos de input el debug en FALSE no me permitira ir editando y que se muestre en la pagina al mismo tiempo.