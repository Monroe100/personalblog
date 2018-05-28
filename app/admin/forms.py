from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,TextAreaField,SubmitField,ValidationError,BooleanField
from wtforms.validators import Required,Email,EqualTo
from ..models import User

class BlogForm(FlaskForm):
    '''
    RegistrationForm class that passes in the required and email validators
    '''
    title = StringField('Title')
    content = TextAreaField('New Blog')
    submit = SubmitField('Submit')