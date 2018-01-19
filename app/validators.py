import re

def validate_username(username):
    username_pattern = re.compile(r'^[a-zA-Z_]+([a-zA-Z0-9]{1,10})$')
    if username_pattern.match(username):
        return True
    return False


def validate_email(email):
    email_pattern = re.compile(
        r'(^[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]+$)')
    if email_pattern.match(email):
        return True
    return False


def validate_password(password):
    password_pattern = re.compile(r'^\w{6,25}$')
    if password_pattern.match(password):
        return True
    return False