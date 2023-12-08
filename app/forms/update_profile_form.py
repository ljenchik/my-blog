from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    info = TextAreaField('Info', validators=[Length(min=0, max=250)])
    profile_image = FileField('Profile image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save')
