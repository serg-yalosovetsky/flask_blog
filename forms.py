from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('name')    
    email = StringField('email', validators=[DataRequired()])    
    password = PasswordField('pass', validators=[DataRequired()])    
    remember_me = BooleanField('remember me')
    submit = SubmitField('login')
    submit2 = SubmitField('register')
        
