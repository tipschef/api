class UserNotAdminException(Exception):
    def __str__(self):
        return 'You\'re not admin'
