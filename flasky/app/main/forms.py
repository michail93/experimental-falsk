from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from flask_wtf import Form
from wtforms.validators import Required, Length, Email, Regexp




class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')