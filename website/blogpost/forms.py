from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired

class SignupForm(FlaskForm):
    name = StringField("Input your name", validators = [DataRequired()])
    username = StringField("Input your username", validators = [DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password1 = PasswordField("Password", validators =[DataRequired()])
    password2 = PasswordField("Confirm your password", validators =[DataRequired()])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    username = StringField("Username:", validators = [DataRequired()])
    password = PasswordField("Password:", validators =[DataRequired()])
    submit = SubmitField("Login")

