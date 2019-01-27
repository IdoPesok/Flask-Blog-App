from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired()])
    imageUrl = StringField('Image URL', validators = [DataRequired()])
    content = TextAreaField('Content', validators = [DataRequired()])
    submit = SubmitField('Post')


class UpdatePostForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired()])
    imageUrl = StringField('Image URL', validators = [DataRequired()])
    content = TextAreaField('Content', validators = [DataRequired()])
    submit = SubmitField('Update')
