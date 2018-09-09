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
		order_by = ('-joined_at',)

#UserMixin es una clase que le da ciertos métodos de autenticación de inicio de sesión, verificación de email, funcionalidad de usuarios anonimos, obtener el id
class Client(UserMixin, BaseModel):
	username = CharField(unique = True)
	email = CharField(unique = True)
	password = CharField(max_length = 120)
	joined_at = DateTimeField(default = datetime.datetime.now)

	def get_posts(self):
		return Post.select().where(Post.user == self)

	@classmethod
	def create_user(self, username, email, password):
		try:
			self.create(
				username = username,
				email = email,
				password = generate_password_hash(password) 
			)
		except IntegrityError:
			pass
			#raise ValueError('User already exists')

class Post(BaseModel):
	user = ForeignKeyField(
		Client,
		related_name = 'posts'
	)
	timestamp = DateTimeField(default = datetime.datetime.now)
	content = TextField()



# usuario = User()
# usuario.create_user(daniel, daniel, daniel)

#usuario = User.create_user(daniel, daniel, daniel)

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Client,Post], safe = True)
	DATABASE.close()