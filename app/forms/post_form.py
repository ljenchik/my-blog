from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = PageDownField('Title', validators=[DataRequired(), Length(min=0, max=250)])
    post = PageDownField('Content', validators=[DataRequired(), Length(min=0, max=2500)])
    submit = SubmitField('Save')
