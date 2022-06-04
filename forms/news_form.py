from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    text = TextAreaField('Текст Новости', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')
