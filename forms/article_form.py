from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired


class ArticleForm(FlaskForm):
    title = StringField('Название статьи', validators=[DataRequired()])
    text = TextAreaField('Текст статьи', validators=[DataRequired()])
    tegs = SelectMultipleField("Теги", choices=['Python', 'HTML', 'ML_learning', 'bd', 'Author', 'Single'],
                               validators=[DataRequired()])
    submit = SubmitField('Отправить статью')


class EditArticleForm(FlaskForm):
    title = StringField('Название статьи')
    text = TextAreaField('Текст статьи')
    submit = SubmitField('Обновить статью')
