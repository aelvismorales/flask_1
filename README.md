## Sobre el Proyecto
Este es una Api que devuelve una lista de comidas separadas en desayuno, almuerzo y cena para un niño de entre 6 a 12 años
según sus necesidades, las cuales se calculan en base a la edad, peso y altura del menor.

### Construido con
* [Flask](https://flask.palletsprojects.com/en/2.1.x/)
* [Flask RestFul](https://flask-restful.readthedocs.io/en/latest/)
* [Pandas](https://pandas.pydata.org/)

## Getting Started
Para poder desarrollar el proyecto, antes debemos de seguir algunos pasos para configurar un ambiente con todas
las dependencias necesarias, y que de esta manera, no tengamos problemas al momento de ejecutarlo localmente.

### Prerequisitos

Primero que nada, se debe de tener instalado Conda en el ordenador donde se desplegará este proyecto. Para ello, 
puede guiarse de la documentación oficial haciendo click [aquí](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

Una vez ya se tenga Conda instalado, podemos continuar con la instalación.

### Instalación (LINUX)

1. Iniciaremos con la clonación del repositorio:
```sh
   git clone https://github.com/TDP-2022-01/dieta-api.git
   cd dieta-api/
```
2. Crearemos un ambiente con Conda de la siguiente manera:
 ```sh
   conda create --name dieta-api python=3.9
 ```
3. Una vez creado el ambiente, debemos de añadir las siguientes variables de entorno al mismo:
 ```sh
   conda activate dieta-api
   conda env config vars set FLASK_APP="entrypoint:app"
   conda env config vars set FLASK_ENV="development"
   conda env config vars set APP_SETTINGS_MODULE="config.default"
 ```
4. Ya que tengamos las varaibles de entorno configuradas, procederemos a reactivarlo con los siguientes comandos:
 ```sh
   conda deactivate
   conda activate dieta-api
 ```
5. Luego, continuamos con la instalación de las dependencias necesarias, las cuales 
 ya se encuentran en el archivo **requirements.txt**, por lo que solo tendríamos que aplicar el siguiente comando:
 ```sh
   pip install -r requirements.txt
 ```
 
 ## Uso
 Cuando ya tengamos el ambiente creado y configurado con las dependencias, ya podremos realizar
 las modificaciones pertinentes. Asimismo, se podrá realizar la ejecución del proyecto con el comando:
  ```sh
   flask run
  ```
 ### Ruta del API
 - api/v1.0/diets?age=10&weight=35.0&height=135&activity=Sedentario&sex=F
