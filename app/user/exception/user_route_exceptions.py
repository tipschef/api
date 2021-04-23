class UserAlreadyExistsException(Exception):
    user_email: str

    def __init__(self, user_email: str):
        self.user_email = user_email

    def __str__(self):
        return f"'{self.user_email}' already used."
