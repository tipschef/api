class BookIdNotFoundException(Exception):

    def __str__(self):
        return 'The given book ID cannot be found'


class UniqueIdDoesNotMatch(Exception):

    def __str__(self):
        return 'The given unique id does not match.'