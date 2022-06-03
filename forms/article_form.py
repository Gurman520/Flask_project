from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired
from data import db_session
from data.tables import Tag

db_session.global_init("db/my_project.db")


class ArticleForm(FlaskForm):
    title = StringField('Название статьи', validators=[DataRequired()])
    text = TextAreaField('Текст статьи', validators=[DataRequired()])
    tegs = SelectMultipleField("Теги", choices=[i.name for i in db_session.create_session().query(Tag)],
                               validators=[DataRequired()])
    submit = SubmitField('Отправить статью')


class EditArticleForm(FlaskForm):
    title = StringField('Название статьи')
    text = TextAreaField('Текст статьи')
    submit = SubmitField('Обновить статью')


class AddTeg(FlaskForm):
    name = StringField('Название Тега')
    submit = SubmitField('Добавить тег')
