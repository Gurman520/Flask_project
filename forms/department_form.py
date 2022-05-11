from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class DeptForm(FlaskForm):
    title = StringField('Название Департамента', validators=[DataRequired()])
    chief = IntegerField('ID начальника', validators=[DataRequired()])
    members = StringField("ID участников", validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])

    submit = SubmitField('Зарегестрировать')
