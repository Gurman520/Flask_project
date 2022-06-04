from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class MessageForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    subject = SelectField('Тема письма', choices=[' Проблема/Баг ', 'Вопрос по работе сайта ', ' Предложение по улучшению работы ', 'Другое'])
    text = TextAreaField('Текст статьи', validators=[DataRequired()])
    submit = SubmitField('Отправить')