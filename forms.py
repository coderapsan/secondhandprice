from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PredictionForm(FlaskForm):
    company = StringField('Car Company Name', validators=[DataRequired()])
    model = StringField('Car Model', validators=[DataRequired()])
    year = IntegerField('Year Made', validators=[DataRequired()])
    showroom = StringField('Purchased Showroom', validators=[DataRequired()])
    engine = SelectField('Engine Type', choices=[('Diesel', 'Diesel'), ('Petrol', 'Petrol'), ('Other', 'Other')],
                         validators=[DataRequired()])
    kms = IntegerField('Kilometers Ran', validators=[DataRequired()])
    submit = SubmitField('Predict Price')
