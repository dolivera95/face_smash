import datetime 
from flask_login import UserMixin
from peewee import *
from flask_bcrypt import generate_password_hash

DATABASE = PostgresqlDatabase(
	'test_db',
	user = "dolivera",
	password = "qaz123PL098",
	host = "localhost"
	)

class BaseModel(Model):
	class Meta:
		database = DATABASE


#UserMixin es una clase que le da ciertos métodos de autenticación de inicio de sesión, verificación de email, funcionalidad de usuarios anonimos, obtener el id
class Client(UserMixin, BaseModel):
	username = CharField(unique = True)
	email = CharField(unique = True)
	password = CharField(max_length = 120)
	joined_at = DateTimeField(default = datetime.datetime.now)

	class Meta:
		order_by = ('-joined_at',)
	#devolver todos los posts de este usuario, es un metodo de instancia porque se neceista saber los posts de UN USUARIO EN PARTICULAR
	def get_posts(self):
		return Post.select().where(Post.user == self)
	#devolver todos los posts de este usuario, es un metodo de instancia porque se neceista saber los posts de UN USUARIO EN PARTICULAR
	def get_stream(self):
		return Post.select().where(Post.user == self)

	def get_following(self):
		"""Los usuarios que estamos siguiendo"""
		return (
			#Seleccionar todos los usuarios que tengan join de id_user on to_user (al usuario que sigo)
			#Seleccionar todos los usuarios cuya relacion hacia un usuario sea hacia mi (el usuario que inicio sesión).
			Client.select().join(
				Relationship, on = Relationship.to_user
			#donde estos usuarios (from_user) tengna el id mio es decir que me sigan
			).where(
				Relationship.from_user == self
			)
		)

	def followers(self):
		"""Obtener los usuarios que me siguen"""
		return (
			#Seleccionar todos los usuarios que tengan join de id_user on to_user (al usuario que sigo)
			#Seleccionar todos los usuarios cuya relacion hacia un usuario sea hacia mi (el usuario que inicio sesión).
			Client.select().join(
				Relationship, on = Relationship.from_user
			#donde estos usuarios (from_user) tengna el id mio es decir que me sigan
			).where(
				Relationship.to_user == self
			)
		)

	@classmethod
	def create_user(self, username, email, password):
		try:
			#Utilizar una transacción para hacer la siguiente operación, pero si esta transacción falla, no se cerrará la db y se lanzará un error.
			with DATABASE.transaction():
				self.create(
					username = username,
					email = email,
					password = generate_password_hash(password) 
				)
		except IntegrityError:
			raise ValueError('User already exists')
			#raise ValueError('User already exists')

class Post(BaseModel):
	user = ForeignKeyField(
		Client,
		related_name = 'posts'
	)
	timestamp = DateTimeField(default = datetime.datetime.now)
	content = TextField()

	class Meta:
		order_by = ('-joined_at',)

class Relationship(BaseModel):
	#del usuario: usuarios a los que yo sigo
	from_user = ForeignKeyField(Client, related_name = 'relationship')
	#al usuario: usuarios a los que me siguen
	to_user = ForeignKeyField(Client, related_name = 'related_to')

	class Meta:
		database = DATABASE
		#Solo un usuario puede ser a un usuario al poner True a los indexes
		indexes = (
			(('from_user', 'to_user'), True),
		)

# usuario = User()
# usuario.create_user(daniel, daniel, daniel)

#usuario = User.create_user(daniel, daniel, daniel)

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Client,Post, Relationship], safe = True)
	DATABASE.close()