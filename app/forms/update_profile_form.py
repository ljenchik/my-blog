from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, FileField, ValidationError
from wtforms.validators import DataRequired, Length
from app.models.models import User


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    info = TextAreaField('About me', validators=[Length(min=0, max=2500)])
    # profile_image = FileField('Profile image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')
