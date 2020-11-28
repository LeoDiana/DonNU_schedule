from app import db


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))  # Назва дисципліни
    group = db.Column(db.String(20))  # Назва групи
    teacher = db.Column(db.String(20))  # Прізвище та ініціали викладача
    room = db.Column(db.String(20))  # Аудиторія [307, 303А, 412, і т.д.]
    lesson_type = db.Column(db.String(10))  # Тип заняття [лек., пр., лаб., і т.д.]
    day = db.Column(db.Integer)  # День, у який проводиться пара (Понеділок[0]-Субота[5])
    lesson_time = db.Column(db.Integer)  # Номер пари у розкладі (1[0]-8[7])

    def __repr__(self):
        return f'{self.day}/{self.lesson_time} | {self.name} | {self.group}'
