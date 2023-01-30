from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from website.models import User


class SignupForm(FlaskForm):
    name = StringField("Input your name", validators = [DataRequired()])
    username = StringField("Input username", validators = [DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password1 = PasswordField("Password", validators =[DataRequired(), EqualTo('password2', message = 'Passwords must match')])
    password2 = PasswordField("Confirm your password", validators =[DataRequired()])
    submit = SubmitField("Sign Up")

    def check_email(self,field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Your email has been registered already!')
    def check_username(self,field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Change username!')

class LoginForm(FlaskForm):
    email = StringField("Email:", validators = [DataRequired(), Email()])
    password = PasswordField("Password:", validators =[DataRequired()])
    submit = SubmitField("Login")

class UpdateUserForm(FlaskForm):
    username = StringField("Your Username:", validators = [DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','jpeg','png'])])
    submit = SubmitField("Update")

    def check_email(self,field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Your email has been registered already!')
    def check_username(self,field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Change username!')