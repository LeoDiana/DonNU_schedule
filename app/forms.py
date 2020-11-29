from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

from app.schedule_from_docx import groups, teachers


class TeacherChoose(FlaskForm):
    teacher_choices = [(t, t) for t in teachers()]
    teacher = SelectField('Викладач', choices=teacher_choices)
    submit = SubmitField('Далі')


class ScheduleFor(FlaskForm):
    schedule_for = SelectField('Розклад для', choices=[('teacher', 'Викладач'), ('group', 'Група')])
    submit = SubmitField('Далі')


def group_name_transform(group):
    g = ''
    for c in group:
        if c == r'/':
            g = g + '!'
        else:
            g = g + c
    return g


class GroupChoose(FlaskForm):
    group_choices = [(group_name_transform(g), g) for g in groups()]
    group = SelectField('Група', choices=group_choices)
    submit = SubmitField('Далі')
