
#custom exceptions to catch unwanted scenarios

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

class EmptyField(Exception):
    pass

class WrongPassword(Exception):
    pass

class EmptyDescription(Exception):
    pass

class UsernameFormatError(Exception):
    pass

class PasswordFormatError(Exception):
    pass

class EmailFormatError(Exception):
    pass 

class RecipeAlreadyNamed(Exception):
    pass 

class CategoryAlreadyNamed(Exception):
    pass 


    