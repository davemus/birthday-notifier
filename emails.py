import os
import smtplib
from email.mime.text import MIMEText
from email.header    import Header


SENDER = os.environ.get('SMTP_LOGIN')
PASSWORD = os.environ.get('SMTP_PASSWORD')


def construct_message(addresses, birthdays):
    birthdays_str = '\n'.join(birthdays)
    plain_text = f"""
Это день - день рождения следующих людей:

{birthdays_str}

Не забудьте поздравить!
    """
    msg = MIMEText(plain_text, 'plain', 'utf-8')
    msg['Subject'] = Header('Напоминание о Днях Рождения в Наланде', 'utf-8')
    msg['From'] = SENDER
    msg['To'] = ", ".join(addresses)
    return msg


def send_emails(addresses, birthdays):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(SENDER, PASSWORD)
    msg = construct_message(addresses, birthdays)
    server.sendmail(SENDER, addresses, msg.as_string())
    server.quit()

