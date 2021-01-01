from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import datetime
from app.common_vars import lessons_time
#from app.schedule_from_docx import event_list
from app.models import Lesson as Lesson_model
from config import Config


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
calendar_id = Config.CALENDAR_ID


example_lesson = {
    'name': 'Мат. аналіз',
    'when': 1,
    'day': 0,
    'where': 'Teams',
    'description': 'Трофименко О. Д.'
}

example_lesson_2 = {
    'name': 'Програмування',
    'when': 4,
    'day': 1,
    'where': 'Teams',
    'description': 'Антонов Ю.С.'
}


def google_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def add_lesson(lesson):
    """
    lesson in format:
    {
        'name': 'Мат. аналіз',
        'when': 1,  # номер пари
        'day': 1, #  0 - Понеділок, 6 - Неділя
        'where': 'Teams',  # 'ауд. 412-Кристал'
        'description': 'Трофименко О. Д.'  # додаткова інформація (ім'я викладача або група) 'Б19_д/113'
        'is_upper_week' True/False
    }
    return: id of created event
    """

    service = google_service()

    start, end = date_time_for_event(lesson['day'], lesson['when'])
    event = {
        'summary': lesson['name'],
        'location': lesson['where'],
        'description': lesson['description'],
        'start': {
            'dateTime': start,
            'timeZone': 'Europe/Kiev',
        },
        'end': {
            'dateTime': end,
            'timeZone': 'Europe/Kiev',
        },
        'recurrence': [
            f'RRULE:FREQ=WEEKLY;COUNT={recurrence_for_event()};INTERVAL=2'
        ],
        """
        'attendees': [
            {'email': 'dianalyvytska@gmail.com'},
        ],
        """        
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 10},
            ],
        },
        'colorId': '9',
    }

    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
    print(f'Event id: {event["id"]}')
    return event["id"]


def event_list(is_for_group, for_whom):
    if is_for_group:
        p = Lesson_model.query.filter_by(group=for_whom).all()
        g_list = [g.group_event_id for g in p]
    else:
        p = Lesson_model.query.filter_by(teacher=for_whom).all()
        g_list = [g.teacher_event_id for g in p]
    return g_list


#TODO confirm subscription by email
def add_attendee(email):
    # will be db with even ids for each group, but now we have this:
    events_id = event_list(True, 'Б19_д/113')

    service = google_service()

    for event_id in events_id:
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        if 'attendees' in event:
            event['attendees'].append({'email': 'dianalyvytska@gmail.com'})
        else:
            event['attendees'] = [{'email': 'dianalyvytska@gmail.com'}]
        updated_event = service.events().update(calendarId=calendar_id,
                                                eventId=event_id,
                                                body=event)\
            .execute()
    print(f'Attendee {email} added')


def date_time_for_event(day, lesson_number):
    """
    :param day: 0 - Monday, 6 - Sunday
    :param lesson_number: from 0 to 7
    :return: (start_dateTime, end_dateTime) in this format '2020-12-13T15:20:00'
    """
    today = datetime.datetime.now().date()
    next_weekday = today + datetime.timedelta(days=((day - today.weekday()) + 7) % 7)
    lesson_time = lessons_time[lesson_number]
    return f'{next_weekday}T{lesson_time[:lesson_time.find("-")]}:00',\
           f'{next_weekday}T{lesson_time[lesson_time.find("-")+1:]}:00'


def recurrence_for_event():
    """
    :return: count of weeks from now till New Year or June
    """
    today = datetime.datetime.now().date()
    if today.month > 6:
        return int((datetime.date(today.year, 12, 31) - today).days / 7)
    else:
        return int((datetime.date(today.year, 6, 1) - today).days / 7)


if __name__ == '__main__':
    #add_lesson(example_lesson_2)
    add_attendee('lyvytska.d@donnu.edu.ua')
