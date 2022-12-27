import os
import datetime
from collections import namedtuple
from database import cursor, connection


cursor.execute(
    'CREATE TABLE IF NOT EXISTS reports ('
        'id SERIAL, '
        'timestamp TIMESTAMP NOT NULL, '
        'is_success BOOLEAN NOT NULL, '
        'message TEXT'
    ');'
)
connection.commit()


Report = namedtuple('Report', 'id timestamp is_success message')


def emails_have_already_been_sent():
    today = datetime.date.today()
    cursor.execute(
        'SELECT * FROM reports '
            'WHERE timestamp::date = %s;',
        (today,)
    )
    reports = cursor.fetchall()
    if not reports:
        return False
    return any(
        report.is_success for report in
        map(lambda x: Report(*x), reports)
    )


def _write_report(*, is_success, message=''):
    now = datetime.datetime.now()
    cursor.execute(
        'INSERT INTO reports '
            '(timestamp, is_success, message) '
            'values (%s, %s, %s);',
        (now, is_success, message)
    )
    connection.commit()


def write_report_on_successful_sending(birthdays_count, notifications_count):
    if birthdays_count and notifications_count:
        message = (
            f'Successfully sent {notifications_count} notification(s) '
            f'on {birthdays_count} birthday(s)'
        )
    elif notifications_count:
        message = 'No birthdays found for this day'
    else:
        message = 'No notification emails configured'
    _write_report(is_success=True, message=message)


def write_report_on_exception(exception):
    _write_report(is_success=False, message=str(exception))
    raise exception
