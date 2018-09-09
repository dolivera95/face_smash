#g es un elemento global para almacenar todo lo que se quiera de la aplicación y será accesible en todos lados
#render_template para renderizar una template de html, flash para desplegar un mensaje despues de la siguiente peticion, url_for para generar una url a un endpoint, redirect para redireccionar a un usuario
from flask import (Flask, g, render_template, render_template, flash, url_for, redirect)
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
import forms

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
login_manager.login_view = 'login'

#Para que sea una función de la misma clase de login_manager
@login_manager.user_loader
#Metodo para cargar el usuario que está logueado
def load_user(userid):
	try:
		#Definir como se obtienen los usuarios en la app
		#models: archivo de modelos, User: el usuario, 
		return models.Client.get(models.Client.id == userid)
	except models.DoesNotExist:
		return None

#Registra una funcion que sea ejecutada antes de cada peticion a la BD, esta funcion debe ser llamada sin ningun argumento
@app.before_request
#Before_request: establecer conexiones con la BD 
def before_request():
	"""Conecta a la base de datos antes de cada request"""
	#hasattr = verifica que el 'g' no tenga el atributo 'db' definido en si mismo
	#A veces puede haber error con el attrr, por lo tanto hay otra opción
	#if  not hasattr(g, 'db'):
	#	g.db = models.DATABASE
	#	g.db.connect()
	#Otra opcion: 
	g.db = models.DATABASE
	#Si la conexión con la BD está cerrada, se vuelve a abrir.
	if g.db.is_closed():
		g.db.connect()
		g.user = current_user

@app.after_request
#Luego de la peticion se tendra una respuesta. en el 90% de ocasiones
def after_request(response):
	"""Cerrarmos la conexión a la bd"""
	g.db.close()
	return response

@app.route('/register', methods = ['GET','POST'])
def register():
	form = forms.RegisterForm()
	#Que se valida con las validaciones realizadas
	if form.validate_on_submit():
		#Si fue valida
		flash('Fuiste registrado!!! :D', 'success')
		models.Client.create_user(
			username = form.username.data,
			email = form.email.data,
			password = form.password.data
		)
		#url_for generará una url para una vista que tiene como parámetro, y redirect va a redireccionar al usuario a esa vista con esa url
		return redirect(url_for('index'))
	#Renderizar el template de reigstro, si no esta registrado aún 
	return render_template('register.html', form = form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
	form = forms.LoginForm()
	if form.validate_on_submit():
		try:
			client = models.Client.get(models.Client.email == form.email.data)
		except	models.DoesNotExist:
			flash('Tu nombre de usuario o contraseña no existen', 'error')
		else:
			if check_password_hash(client.password, form.password.data):
				login_user(client)
				flash('Has iniciado sesión', 'success')
				return redirect(url_for('index'))
	return render_template('login.html', form = form) 

@app.route('/logout')
#login_required = permite que solo se ejecute la vista solo si el usuario ya está logueado.
@login_required
def logout():
	logout_user()
	flash('Has salido de tu sesión :(', 'success')
	return redirect(url_for('index'))

@app.route("/new_post", methods = ['GET', 'POST'])
def post():
	form = forms.PostForm()
	if form.validate_on_submit():
		models.Post.create(
			#_get_current_object() = entrega el usuario actual de la sesión.
			user = g.user._get_current_object(), 
			content = form.content.data.strip()
		)
		flash('Mensaje posteado! :D', 'success')
		return redirect(url_for('index'))
	return render_template('post.html', form = form)


@app.route('/')
def index():
	return 'Hey'

if __name__ == '__main__':
	models.initialize()
	models.Client.create_user(
		username = 'dolivera',
		email = 'dolivera95@gmail.com',
		password = 'dolivera95',
	)
	app.run(debug = DEBUG, host = HOST, port = PORT)