from flask_wtf import FlaskForm

from models import Client 
from wtforms import (StringField, PasswordField)
from wtforms.validators import (DataRequired, ValidationError, Email, Regexp, Length, EqualTo)

#Un validador personalizado para verificar si el usuario ya existe antes de inscribirlo.
def name_exists(form, field):
	if Client.select().where(Client.username == field.data).exists():
		raise ValidationError('Ya existe un usuario con ese nombre :( ')

def email_exists(form, field):
	if Client.select().where(Client.email == field.data).exists():
		raise ValidationError('Ya existe un usuario con ese email :o ')

#Clase para el registro de usuarios, hereda atributos y funciones de la clase FlaskForm
class RegisterForm(FlaskForm):
	#Ingresar todos los campos que el usuario necesita llenar para inscribirse
	username = StringField(
		#1er parametro: nombre del campo que se va a desplegar al usuario
		'Username',
		#2do parametro: los validadores que se aceptaran para inscribir
		validators = [
			DataRequired(),
			Regexp(
				r'^[a-zA-Z0-9_]+$'
			),
			name_exists
		]
	)

	email = StringField(
		'Email',
		validators = [
			DataRequired(),
			Email(),
			email_exists
		]
	)

	password = PasswordField(
		'Password',
		validators = [
			DataRequired(),
			Length(min = 4),
			EqualTo('password2', message = 'Los password deben coincidir')
		]
	)

	password2 = PasswordField(
		'Confirm Password',
		validators = [
			DataRequired()]
	)

class LoginForm(Form):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])