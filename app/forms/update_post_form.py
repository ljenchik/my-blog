from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import Length


class UpdatePostForm(FlaskForm):
    post = TextAreaField('Update or delete post', validators=[Length(min=0, max=2500)])
    submit = SubmitField('Save')
