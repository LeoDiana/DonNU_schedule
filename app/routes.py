from app import schedule_app as sapp
from flask import render_template, redirect, url_for, request
from app.forms import ScheduleFor, group_name_transform

from app.schedule_from_docx import group_schedule, teacher_schedule, groups, teachers
from app.common_vars import lessons_time
from app.googlecalendar import add_attendee


@sapp.route('/', methods=['GET', 'POST'])
@sapp.route('/index', methods=['GET', 'POST'])
def choose():
    form = ScheduleFor()
    t = teachers()
    g = groups()
    if form.validate_on_submit():
        print(form.schedule_for.data)
        if form.schedule_for.data == 'group':
            return redirect(url_for('group_choose'))
        if form.schedule_for.data == 'teacher':
            return redirect(url_for('teacher_choose'))
    return render_template('choose.html', form=form, teachers=t, groups=g)


@sapp.route('/handle_data', methods=['POST'])
def handle_data():
    cat1 = request.form['category1']
    cat2 = request.form['category2']
    if cat1 == 'groups':
        cat2 = group_name_transform(cat2)
        return redirect('group/' + cat2)
    elif cat1 == 'teachers':
        return redirect('teacher/' + cat2)


@sapp.route('/group/<group_name>')
def group(group_name):
    group_name = group_name.replace('!', r'/')
    schedule_for = {'name': f'групи {group_name}'}
    upper_schedule, lower_schedule = group_schedule(group_name)
    return render_template('schedule.html', schedule_for=schedule_for,
                           upper_table=upper_schedule, lower_table=lower_schedule,
                           time=lessons_time)


@sapp.route('/teacher/<teacher_name>')
def teacher(teacher_name):
    schedule_for = {'name': f'{teacher_name}'}
    upper_schedule, lower_schedule = teacher_schedule(teacher_name)
    return render_template('schedule.html', schedule_for=schedule_for,
                           upper_table=upper_schedule, lower_table=lower_schedule,
                           time=lessons_time)


@sapp.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    schedule_for = request.form['schedule_for']
    add_attendee(email, schedule_for)
    return redirect('index')
