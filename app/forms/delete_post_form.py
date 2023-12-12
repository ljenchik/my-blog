from flask_wtf import FlaskForm
from wtforms import SubmitField


class DeletePostForm(FlaskForm):
    submit = SubmitField('Delete', render_kw={'class':'btn btn-default text-right'})

