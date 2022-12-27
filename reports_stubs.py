def emails_have_already_been_sent():
    return False


def write_report_on_successful_sending(birthdays_count, notifications_count):
    print(f'Successfully send {notifications_count} emails on {birthdays_count} birthdays')


def write_report_on_exception(exception):
    print(exception)
