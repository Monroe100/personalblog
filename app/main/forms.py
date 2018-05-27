from wtforms.validators import Required
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField

class BlogForm(FlaskForm):
    title = StringField('Title',validators=[Required()])
    content = TextAreaField('New Blog',validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment_section = TextAreaField('Comment', validators=[Required()])
    submit = SubmitField('Submit')

class SubscriptionForm(FlaskForm):
    email = TextAreaField('Email (required)', validators=[Required()])
    submit = SubmitField('Submit')
