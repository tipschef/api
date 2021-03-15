class SecretManagerCannotBeReachedException(Exception):

    def __str__(self):
        return 'Secret manager cannot be reached. Verify your input data'
