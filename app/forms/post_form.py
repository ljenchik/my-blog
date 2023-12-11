from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    post = TextAreaField('Create a new post', validators=[DataRequired(), Length(min=0, max=2500)])
    submit = SubmitField('Save')
