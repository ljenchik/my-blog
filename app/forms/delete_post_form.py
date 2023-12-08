from flask_wtf import FlaskForm
from wtforms import SubmitField


class DeletePostForm(FlaskForm):
    submit = SubmitField('Delete')
