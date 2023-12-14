from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class DropdownForm(FlaskForm):
      sorting_options = SelectField('', choices=['Sort by', 'Newest first', 'Oldest first', 'Most popular'])
      # submit=SubmitField('Submit')
