class UserBaseException(Exception):
    def __init__(self, username: str):
        self.username = username


class UserAlreadyExistsException(UserBaseException):
    pass


class UserDoesNotExistException(UserBaseException):
    pass


class UserInvalidCredentialsException(Exception):
    pass
