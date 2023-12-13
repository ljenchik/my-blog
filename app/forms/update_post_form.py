from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import Length, DataRequired
from flask_pagedown.fields import PageDownField


class UpdatePostForm(FlaskForm):
    title = PageDownField('Title', validators=[DataRequired(), Length(min=0, max=250)])
    post = PageDownField('', validators=[DataRequired(), Length(min=0, max=2500)])
    submit = SubmitField('Save')
