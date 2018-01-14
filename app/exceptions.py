
""" custom exceptions to catch unwanted scenarios"""

class ResourceAlreadyExists(Exception):
    pass

class YouDontOwnResource(Exception):
    pass

class PasswordEmpty(Exception):
    pass

class UsernameEmpty(Exception):
    pass 

class EmailEmpty(Exception):
    pass

class NameEmpty(Exception):
    pass
