import datetime 
from flask_login import UserMixin
from peewee import *
from flask_bcrypt import generate_password_hash

DATABASE = PostgresqlDatabase(
	'social',
	user = "postgres",
	password = "258258258q",
	host = "localhost"
	)

class BaseModel(Model):
	class Meta:
		database = DATABASE
		order_by = ('-joined_at')
#UserMixin es una clase que le da ciertos métodos de autenticación de inicio de sesión, verificación de email, funcionalidad de usuarios anonimos, obtener el id
class User(UserMixin, BaseModel):
	username = CharField(unique = True)
	email = CharField(unique = True)
	password = CharField(max_length = 120)
	joined_at = DateFimeField(default = datetime.datetime.now)

	@classmethod
	def create_user(self, usename, email, password):
		try:
			self.create(
				username = username,
				email = email,
				password = generate_password_hash(password) 
			)
		except IntegrityError:
			raise ValueError('User already exists')

# usuario = User()
# usuario.create_user(daniel, daniel, daniel)

#usuario = User.create_user(daniel, daniel, daniel)

