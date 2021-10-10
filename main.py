import datetime

from data import (
    retrieve_email_addresses,
    retrieve_birthday_people,
)
from reports import (
    emails_have_already_been_sent,
    write_report_on_successful_sending,
    write_report_on_exception,
)
from emails import send_emails



if __name__ == '__main__':
    try:
        if not emails_have_already_been_sent():
            birthday_boys_and_girls = retrieve_birthday_people()
            notified_people = retrieve_email_addresses()
            if birthday_boys_and_girls and notified_people:
                send_emails(
                    notified_people,
                    birthday_boys_and_girls,
                )
            write_report_on_successful_sending()
    except Exception as e:
        write_report_on_exception(str(e))

