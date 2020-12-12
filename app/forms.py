from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class ScheduleFor(FlaskForm):
    submit = SubmitField('Далі')


def group_name_transform(group):
    g = ''
    for c in group:
        if c == r'/':
            g = g + '!'
        else:
            g = g + c
    return g
