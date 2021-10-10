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
            send_emails(
                retrieve_email_addresses(),
                retrieve_birthday_people(),
            )
            write_report_on_successful_sending()
    except Exception as e:
        write_report_on_exception(str(e))

