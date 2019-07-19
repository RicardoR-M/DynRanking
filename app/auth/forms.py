from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError

from ..models import User


class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(1, 10)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    username = StringField('Usuario',
                           validators=[DataRequired(),
                                       Length(1, 20),
                                       Regexp('^[A-Za-z0-9]*$', 0, 'Usuarios solo deben contener letras o números')])
    password = PasswordField('Contraseña',
                             validators=[DataRequired(),
                                         EqualTo('password2', message='Las contraseñas deben de ser iguales')])
    password2 = PasswordField('Confirmar Contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrar')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('El usuario ya se encuentra registrado.')
