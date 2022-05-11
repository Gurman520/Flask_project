from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    email = StringField('Login/Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    s_name = StringField('Фамилия', validators=[DataRequired()])
    f_name = StringField('Имя', validators=[DataRequired()])
    country = StringField("Страна", validators=[DataRequired()])

    submit = SubmitField('Зарегестрироваться')
