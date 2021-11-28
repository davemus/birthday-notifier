import os
from collections import namedtuple
from datetime import date, datetime
from itertools import chain
from googleapiclient.discovery import build


spreadsheet_birthdays_id = os.environ['GOOGLE_SPREADSHEET_BIRTHDAYS_ID']
birthdays_range = "B1:C1000"

spreadsheet_emails_id = os.environ['GOOGLE_SPREADSHEET_NOTIFICATION_EMAILS_ID']
emails_range = "'Получатели нотификаций'!A1:A1000"


API_KEY = os.environ['GOOGLE_API_KEY']
service = build('sheets', 'v4', developerKey=API_KEY)


Person = namedtuple('Person', 'full_name birthday')


def parse_time(string_f):
    """
    Parses time in row. Time must be in format 'dd.mm.REST...'

    >>> parse_time('28.11.2001')
    datetime.datetime(2000, 11, 28, 0, 0)
    >>> parse_time('28.11.xxxx')
    datetime.datetime(2000, 11, 28, 0, 0)
    """
    day, month = [int(part) for part in string_f.split('.')[:2]]
    placeholder_year = 2000
    return datetime(day=day, month=month, year=placeholder_year)


def retrieve_email_addresses():
    request = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_emails_id,
        range=emails_range,
    )
    raw_response = request.execute()
    return list(chain.from_iterable(raw_response.get('values', [])))


def compare_days(date1, date2):
    return date1.month == date2.month and date1.day == date2.day


def retrieve_birthday_people():
    request = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_birthdays_id,
        range=birthdays_range,
    )
    raw_response = request.execute()
    def parse_row(row):
        try:
            return Person(
                row[0],
                parse_time(row[1]),
            )
        except:
            return None
    people = [
        parse_row(row) for row in
        raw_response.get('values', [])
    ]
    today = date.today()
    return [
        person.full_name for person in people
        if person is not None and compare_days(person.birthday, today)
    ]

