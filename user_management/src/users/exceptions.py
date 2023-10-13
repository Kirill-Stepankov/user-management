class UserAlreadyExistsException(Exception):
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email
