from app import schedule_app as sapp
from flask import render_template, redirect, url_for
from app.forms import GroupChoose, ScheduleFor, TeacherChoose


from app.schedule_from_docx import group_schedule, teacher_schedule


lessons_time = ['8:00-9:20', '9:30-10:50', '11:20-12:40', '12:50-14:10',
                '14:20-15:40', '15:50-17:10', '17:20-18:40', '18:50-20:10']


@sapp.route('/', methods=['GET', 'POST'])
@sapp.route('/index', methods=['GET', 'POST'])
def choose():
    form = ScheduleFor()
    if form.validate_on_submit():
        print(form.schedule_for.data)
        if form.schedule_for.data == 'group':
            return redirect(url_for('group_choose'))
        if form.schedule_for.data == 'teacher':
            return redirect(url_for('teacher_choose'))
    return render_template('choose.html', form=form)


@sapp.route('/group', methods=['GET', 'POST'])
def group_choose():
    form = GroupChoose()
    if form.validate_on_submit():
        return redirect('group/'+form.group.data)
    return render_template('groupchoose.html', form=form)


@sapp.route('/teacher', methods=['GET', 'POST'])
def teacher_choose():
    form = TeacherChoose()
    if form.validate_on_submit():
        return redirect('teacher/'+form.teacher.data)
    return render_template('teacherchoose.html', form=form)


@sapp.route('/group/<group_name>')
def group(group_name):
    group_name = group_name.replace('!', r'/')
    schedule_for = {'name': f'групи {group_name}'}
    schedule = group_schedule(group_name)
    return render_template('schedule.html', schedule_for=schedule_for, table=schedule, time=lessons_time)


@sapp.route('/teacher/<teacher_name>')
def teacher(teacher_name):
    schedule_for = {'name': f'{teacher_name}'}
    schedule = teacher_schedule(teacher_name)
    return render_template('schedule.html', schedule_for=schedule_for, table=schedule, time=lessons_time)
