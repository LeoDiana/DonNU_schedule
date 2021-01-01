from docx.api import Document
from app.models import Lesson as Lesson_model
from app import db

from app.googlecalendar import add_lesson


class Lesson:
    def __init__(self, name, for_whom, lesson_type, classroom):
        self.name = name
        self.for_whom = for_whom
        self.lesson_type = lesson_type
        self.classroom = classroom


folder = '../docx/'
filename = '113+122_М_2 курс.docx'


def create_empty_schedule():
    sch = []
    for i in range(8):
        day = []
        for j in range(6):
            day.append(None)
        sch.append(day)
    return sch


def convert_day_to_int(day):
    day = ''.join(e for e in day if e.isalnum())
    if day == 'Понеділок':
        return 0
    if day == 'Вівторок':
        return 1
    if day == 'Середа':
        return 2
    if day == 'Четвер' or day == 'Четверг':
        return 3
    if day == 'Пятниця':
        return 4
    if day == 'Субота':
        return 5
    raise ValueError('Неправильний день тижня')


def convert_lesson_to_int(lesson):
    lesson = lesson.replace('\n', '')
    if lesson == 'І':
        return 0
    if lesson == 'ІІ':
        return 1
    if lesson == 'ІІІ':
        return 2
    if lesson == 'ІV':
        return 3
    if lesson == 'V':
        return 4
    if lesson == 'VІ':
        return 5
    if lesson == 'VІІ':
        return 6
    if lesson == 'VІІІ':
        return 7
    raise ValueError('Неправильна пара')


def clean_teacher(teacher):
    if teacher == '':
        return teacher
    upper_count = 0
    last = 0
    for i, c in enumerate(teacher):
        if c in 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЮЯ':
            upper_count += 1
        if upper_count == 3:
            last = i
            break
    return teacher[:last+1]+'.'


def add_to_db_from_docx(filepath=r'D:\Git\DonNU_schedule\docx\111_2 курс.docx', groups_in_doc=1):
    print(filepath)
    document = Document(filepath)
    is_upper_week = False
    for table in document.tables:
        is_upper_week = not is_upper_week
        group = ['', '']

        for i, row in enumerate(table.rows):
            text = []

            for cell in row.cells:
                text.append(cell.text)

            if i == 0:
                if groups_in_doc == 2:
                    group = [text[2], text[6]]
                else:
                    group = [text[2]]
            if i in [0, 1]:
                continue

            day = convert_day_to_int(text[0])
            lesson_time = convert_lesson_to_int(text[1])

            for i in range(groups_in_doc):
                if text[2+4*i] == text[3+4*i]:  # ДВВС
                    text[3+4*i] = text[4+4*i] = text[5+4*i] = ''
                if text[4+4*i] == 'Microsoft Teams':
                    text[4+4*i] = 'Teams'

                if text[2+4*i]:
                    name = text[2+4*i]
                    teacher = clean_teacher(text[5+4*i])
                    lesson_type = text[3+4*i]
                    room = text[4+4*i]

                    group_event_id = add_lesson({
                        'name': lesson_type + name,
                        'when': lesson_time,
                        'day': day,
                        'where': room,
                        'description': teacher,
                        'is_upper_week': is_upper_week
                    })
                    teacher_event_id = add_lesson({
                        'name': lesson_type + name,
                        'when': lesson_time,
                        'day': day,
                        'where': room,
                        'description': group[i],
                        'is_upper_week': is_upper_week
                    })

                    lesson = Lesson_model(day=day, lesson_time=lesson_time, group=group[i],
                                          name=name, lesson_type=lesson_type,
                                          room=room, teacher=teacher,
                                          teacher_event_id=teacher_event_id,
                                          group_event_id=group_event_id,
                                          is_upper_week=is_upper_week)
                    db.session.add(lesson)
    db.session.commit()


def print_db():
    print(Lesson_model.query.filter_by(name='Методи обчислень').all())


def group_schedule(group):
    schedule_list = Lesson_model.query.filter_by(group=group).all()
    table_schedule_upper = create_empty_schedule()
    table_schedule_lower = create_empty_schedule()
    for lesson in schedule_list:
        new_lesson_model = Lesson(name=lesson.name, for_whom=lesson.teacher,
                                  lesson_type=lesson.lesson_type, classroom=lesson.room)
        if lesson.is_upper_week:
            table_schedule_upper[lesson.lesson_time][lesson.day] = new_lesson_model
        else:
            table_schedule_lower[lesson.lesson_time][lesson.day] = new_lesson_model
    return table_schedule_upper, table_schedule_lower


def teacher_schedule(teacher):
    schedule_list = Lesson_model.query.filter_by(teacher=teacher).all()
    table_schedule_upper = create_empty_schedule()
    table_schedule_lower = create_empty_schedule()
    for lesson in schedule_list:
        new_lesson_model = Lesson(name=lesson.name, for_whom=[lesson.group],
                                  lesson_type=lesson.lesson_type, classroom=lesson.room)
        if lesson.is_upper_week:
            if table_schedule_upper[lesson.lesson_time][lesson.day]:
                if lesson.group not in table_schedule_upper[lesson.lesson_time][lesson.day].for_whom:
                    table_schedule_upper[lesson.lesson_time][lesson.day].for_whom.append(lesson.group)
                continue
            table_schedule_upper[lesson.lesson_time][lesson.day] = new_lesson_model
        else:
            if table_schedule_lower[lesson.lesson_time][lesson.day]:
                if lesson.group not in table_schedule_lower[lesson.lesson_time][lesson.day].for_whom:
                    table_schedule_lower[lesson.lesson_time][lesson.day].for_whom.append(lesson.group)
                continue
            table_schedule_lower[lesson.lesson_time][lesson.day] = new_lesson_model

    return table_schedule_upper, table_schedule_lower


def delete_db():
    #Lesson_model.query.delete()
    #Event_model.query.delete()
    #db.session.commit()
    #db.create_all()
    #db.session.commit()
    pass


def teachers():
    p = Lesson_model.query.with_entities(Lesson_model.teacher).distinct().all()
    t_list = [t[0] for t in p if t[0]]
    return t_list


def groups():
    p = Lesson_model.query.with_entities(Lesson_model.group).distinct().all()
    g_list = [g[0] for g in p if g[0]]
    return g_list


if __name__ == '__main__':
    #db.create_all()
    add_to_db_from_docx()
    #add_lesson(example_lesson_2)
    #delete_db()
    #print(groups())
    #print(event_list(True, 'Б19_д/113'))
    #print(group_schedule('Б19_д/113'))
    pass
