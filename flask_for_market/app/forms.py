from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class RegisterForm(FlaskForm):
    username = StringField(label='User Name')
    email_address = StringField(label='Email Address')
    password = PasswordField(label='Password')
    password_confirmation = PasswordField(label='Confirm Password')
    submit = SubmitField(label='Create Account')