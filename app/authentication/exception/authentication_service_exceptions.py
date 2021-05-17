class WrongCredentialException(Exception):

    def __str__(self):
        return f'Wrong credentials were given !'
