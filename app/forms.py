from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField,IntegerField,FileField
from wtforms.validators import InputRequired, Required
from flask_wtf.file import FileField, FileAllowed, FileRequired, DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class AddProfile(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    firstname = StringField('Firstname', validators=[InputRequired()])
    lastname= StringField('Lastname', validators=[InputRequired()])
    gender= SelectField('Gender', choices=[('Male','Male'),('Female','Female')], validators=[Required()])
    age= IntegerField ('Age', validators=[InputRequired])
    biography= StringField('Biography', validators=[InputRequired()])
    image=FileField('Image',validators=[FileRequired(), FileAllowed(['jpg,png'], 'Images Only!')])
    