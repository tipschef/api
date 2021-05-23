class UserAlreadyExistsException(Exception):
    user_email: str

    def __init__(self, user_email: str):

        self.user_email = user_email

    def __str__(self):
        return f"'{self.user_email}' already used."


class UsernameAlreadyExistsException(Exception):
    username: str

    def __init__(self, username: str):

        self.username = username

    def __str__(self):
        return f"'{self.username}' already used."


class UserNotFoundException(Exception):
    user_id: int

    def __init__(self, user_id: int):

        self.user_id = user_id

    def __str__(self):
        return f"User with id='{self.user_id}' not found."
