from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import Length, DataRequired


class UpdatePostForm(FlaskForm):
    post = TextAreaField('', validators=[DataRequired(), Length(min=0, max=2500)])
    submit = SubmitField('Save')
