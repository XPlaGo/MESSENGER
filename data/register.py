from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    password_again = PasswordField('Repeat password:', validators=[DataRequired()])
    name = StringField('Nickname:', validators=[DataRequired()])
    about = TextAreaField("Something about you:")
    submit = SubmitField('Register')
