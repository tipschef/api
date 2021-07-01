class UserNotPartnerException(Exception):
    username: str

    def __init__(self, username: str):
        self.username = username

    def __str__(self):
        return f"'{self.username}' isn't partner"


class AlreadySubscribedToUser(Exception):
    username: str

    def __init__(self, username: str):
        self.username = username

    def __str__(self):
        return f"'Already subscribed to user {self.username}'"


class TierDoesNotExist(Exception):
    tier: str

    def __init__(self, tier: str):
        self.tier = tier

    def __str__(self):
        return f"'Tier does not exist {self.tier}'"
