from wtforms import Form, TextField, BooleanField, PasswordField
from wtforms.validators import InputRequired

class LoginForm(Form):
    username = TextField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
