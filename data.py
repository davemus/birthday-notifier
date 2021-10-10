import os
from collections import namedtuple
from datetime import date, datetime
from itertools import chain
from googleapiclient.discovery import build


spreadsheet_id = os.environ['GOOGLE_SPREADSHEET_ID']
birthdays_range = "'Дни рождения'!A2:B1000"
emails_range = "'Получатели нотификаций'!A1:A1000"


API_KEY = os.environ['GOOGLE_API_KEY']
service = build('sheets', 'v4', developerKey=API_KEY)


Person = namedtuple('Person', 'full_name birthday')


def retrieve_email_addresses():
    request = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=emails_range,
    )
    raw_response = request.execute()
    return list(chain.from_iterable(raw_response.get('values', [])))


def compare_days(date1, date2):
    return date1.month == date2.month and date1.day == date2.day


def retrieve_birthday_people():
    request = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=birthdays_range,
    )
    raw_response = request.execute()
    parse_date = lambda datestr: datetime.strptime(datestr, '%d.%m.%Y')
    people = list(
        map(
            lambda x: Person(x[0], parse_date(x[1])),
            raw_response.get('values', [])
        )
    )
    today = date.today()
    return [
        person for person in people
        if compare_days(person.birthday, today)
    ]

