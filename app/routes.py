from app import schedule_app as sapp
from flask import render_template


from app.schedule_from_docx import create_schedule


@sapp.route('/')
@sapp.route('/index')
def index():
    group = {'name': 'ПМ-19'}
    lessons_time = ['8:00-9:20', '9:30-10:50', '11:20-12:40', '12:50-14:10',
                    '14:20-15:40', '15:50-17:10', '17:20-18:40', '18:50-20:10']
    days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
    pm_schedule = []
    for i in range(8):
        day = []
        for j in range(6):
            day.append(None)
        pm_schedule.append(day)

    pm_schedule[0][0] = Lesson('Алгоритми', 'Вєтров О.С.', 'лек', '307')
    pm_schedule[1][0] = Lesson('Програмування', 'Антонов Ю.С.', 'лек', '307')
    pm_schedule[2][0] = Lesson('Методи', 'Довбня К.М.', 'лек', '307')
    pm_schedule[3][0] = Lesson('Англійська', 'Дакалюк О.О.', 'пр', '307')

    pm_schedule[0][1] = Lesson('Фотозйомка', 'Родигін К.М.', 'пр', '307')
    pm_schedule[3][1] = Lesson('Методи', 'Довбня К.М.', 'пр', '307')
    pm_schedule[4][1] = Lesson('Програмування', 'Антонов Ю.С.', 'пр', '307')
    pm_schedule[5][1] = Lesson('Алгоритми', 'Вєтров О.С.', 'пр', '307')

    pm_schedule[2][2] = Lesson('Диф. рівння', 'Горбань Ю.С.', 'пр', '307')
    pm_schedule[3][2] = Lesson('Диф. рівння', 'Горбань Ю.С.', 'пр', '307')

    pm_schedule[1][4] = Lesson('Мат аналіз', 'Трофименко О.Д.', 'пр', '307')
    pm_schedule[2][4] = Lesson('Мат аналіз', 'Трофименко О.Д.', 'пр', '307')


    pm_schedule = create_schedule(filepath=r'D:\Git\DonNU_schedule\app\sch.docx')
    print('**************'+pm_schedule[0][1].name)


    return render_template('index.html', group=group, table=pm_schedule, time=lessons_time, days=days)


class Lesson:
    def __init__(self, name, teacher, lesson_type, classroom):
        self.name = name
        self.teacher = teacher
        self.lesson_type = lesson_type
        self.classroom = classroom



#sche = create_schedule('sch.docx')
#print(sche)

