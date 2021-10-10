import os
import datetime


SUCCESS_REPORT_FILE = 'send_dates'
ERRORS_REPORT_FILE = 'errors'


def emails_have_already_been_sent():
    try:
        with open(SUCCESS_REPORT_FILE, 'r') as f:
            last_line = f.readlines()[-1]
        last_date = datetime.date.fromisoformat(last_line)
        return last_date == datetime.date.today()
    except:
        return False


def write_report_on_successful_sending():
    last_date = datetime.date.today().isoformat()
    try:
        with open(SUCCESS_REPORT_FILE, 'a') as f:
            f.write(last_date)
            f.write('\n')
    except Exception as e:
        write_report_on_exception(str(e))


def write_report_on_exception(text):
    with open(ERRORS_REPORT_FILE, 'w') as f:
        f.write(text)

