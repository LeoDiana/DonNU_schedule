from docx.api import Document



class Lesson:
    def __init__(self, name, teacher, lesson_type, classroom):
        self.name = name
        self.teacher = teacher
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


def create_schedule(filepath=r'D:\Git\DonNU_schedule\app\sch.docx'):#(filepath=folder+filename):
    print(filepath)
    document = Document(filepath)
    table = document.tables[0]

    group_1 = create_empty_schedule()
    group_2 = create_empty_schedule()

    for i, row in enumerate(table.rows):
        text = []

        for cell in row.cells:
            text.append(cell.text)
        #print(text)

        if i in [0, 1]:
            continue

        day = convert_day_to_int(text[0])
        lesson = convert_lesson_to_int(text[1])

        if text[2] == text[3]:#ДВВС
            text[3] = text[4] = text[5] = ''
        if text[4] == 'Microsoft Teams':
            text[4] = 'Teams'

        if text[2]:
            group_1[lesson][day] = Lesson(name=text[2], lesson_type=text[3],
                                          classroom=text[4], teacher=clean_teacher(text[5]))
    return group_1


#print(create_schedule())


