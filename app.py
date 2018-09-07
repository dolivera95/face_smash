#g es un elemento global para almacenar todo lo que se quiera de la aplicación y será accesible en todos lados
from flask import Flask, g
from flask_login import LoginManager

import models 

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
#Llave secreta para diferenciar la app de otras que están en la web. Es requerido por el LoginManager
#Si la llave es puesta, los componentes criptográficos van a utilizarlo para crear cookies y otras cosas. Los inicios de seśión se manejan con cookies que  son guardas en los navegadores utilizados por los usuarios
app.secret_key = 'lkjflkdDLK!?FJ0D-_92231,-.29SDLK123sad,.-..'

login_manager = LoginManager()
#LoginManager para manejar las sesiones en la aplicación 'app'
login_manager.init_app(app)
#Decir cuál va a ser la vista llamada y desplegada al usuario cuando se quiera iniciar sesión cuando sean redirigidos
login_manager.login_view('login')

#Para que sea una función de la misma clase de login_manager
@login_manager.user_loader
#Metodo para cargar el usuario que está logueado
def load_user(userid):


#Registra una funcion que sea ejecutada antes de cada peticion a la BD, esta funcion debe ser llamada sin ningun argumento
@app.before_request
#Before_request: establecer conexiones con la BD 
def before_request():
	"""Conecta a la base de datos antes de cada request"""
	#hasattr = verifica que el 'g' no tenga el atributo 'db' definido en si mismo
	if  not hasattr(g, 'db'):
		g.db = models.DB
		g.db.connect()

@app.after_request
#Luego de la peticion se tendra una respuesta. en el 90% de ocasiones
def after_request(response):
	"""Cerrarmos la conexión a la bd"""
	g.db.close()
	return response

if __name__ == '__main__':
	app.run(debug = DEBUG, host = HOST, port = PORT)