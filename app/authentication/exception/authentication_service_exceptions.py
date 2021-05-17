class WrongCredentialException(Exception):

    def __str__(self):
        return 'Wrong credentials were given !'
