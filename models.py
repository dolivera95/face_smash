import datetime 
from flask_login import UserMixin
from peewee import *

db = PostgresqlDatabase(
	'social',
	user = "postgres",
	password = "258258258q",
	host = "localhost"
	)

class BaseModel(Model):
	class Meta:
		database = db
#UserMixin es una clase que le da ciertos métodos de autenticación de inicio de sesión, verificación de email, funcionalidad de usuarios anonimos, obtener el id
class User(UserMixin, BaseModel):
	username = CharField(unique = True)
	email = CharField(unique = True)
	password = CharField(max_length = 120)
	joined_at = DateFimeField(default = datetime.datetime.now)

