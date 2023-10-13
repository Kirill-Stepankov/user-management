class UserDoesNotExistException(Exception):
    def __init__(self, username: str):
        self.username = username


class UserInvalidCredentialsException(Exception):
    def __init__(self, username: str):
        self.username = username
