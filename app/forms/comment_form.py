from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class CommentForm(FlaskForm):
    content = TextAreaField('Add a comment', validators=[DataRequired(), Length(min=0, max=1000)])
    submit = SubmitField('Add comment')
