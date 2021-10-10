def retrieve_email_addresses():
    email = '64726f7a646f76756440676d61696c2e636f6d'
    return [str(bytes.fromhex(email), encoding='utf-8')]


def retrieve_birthday_people():
    return ['Кто-то Важный', 'Важный Кто-то']

