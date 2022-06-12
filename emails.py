import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.header    import Header


SERVER = os.environ['SMTP_SERVER']
PORT = os.environ['SMTP_PORT']
SENDER = os.environ['SMTP_LOGIN']
PASSWORD = os.environ['SMTP_PASSWORD']


def construct_message(addresses, birthdays):
    birthdays_str = '\n'.join(birthdays)
    plain_text = f"""
Это день - день рождения следующих людей:

{birthdays_str}
    """
    msg = MIMEText(plain_text, 'plain', 'utf-8')
    msg['Subject'] = Header('Напоминание о Днях Рождения в Наланде', 'utf-8')
    msg['From'] = SENDER
    msg['To'] = ", ".join(addresses)
    return msg


def send_emails(addresses, birthdays):
    server = smtplib.SMTP(SERVER, PORT)
    context = ssl.create_default_context()
    server.starttls(context=context)
    server.login(SENDER, PASSWORD)
    msg = construct_message(addresses, birthdays)
    server.sendmail(SENDER, addresses, msg.as_string())
    server.quit()

