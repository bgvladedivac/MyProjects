from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class SignUpForm(FlaskForm):
    username = StringField("Username", [
        DataRequired(), Length(min=4, message=("Your username is too short"))])

    password = PasswordField("Password", [
        DataRequired(),
        Length(min=8, message=(
            "Your password is too short, must be at least 8 characters")),
        EqualTo("confirm", message='Passwords must match')])

    confirm = PasswordField("Repeat Password")

    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField("Username", [
        DataRequired(), Length(min=4, message=("Your username is too short"))])

    password = PasswordField("Password", [
        DataRequired(),
        Length(min=8, message=(
            "Your password is too short, must be at least 8 characters"))])

    submit = SubmitField("Login")


class AddTeam(FlaskForm):
    team = StringField("Team", [DataRequired()])
    submit = SubmitField("Add")
