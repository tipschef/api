class UserNotPartnerException(Exception):
    username: str

    def __init__(self, username: str):
        self.username = username

    def __str__(self):
        return f"'{self.username}' isn't partner"
