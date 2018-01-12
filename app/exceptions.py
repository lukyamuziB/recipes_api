
""" custom exceptions to catch unwanted scenarios"""

class ResourceAlreadyExists(Exception):
    pass

class YouDontOwnResource(Exception):
    pass
