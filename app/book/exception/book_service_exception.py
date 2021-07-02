class BookIdNotFoundException(Exception):

    def __str__(self):
        return 'The given book ID cannot be found'


class AlreadyHaveBookException(Exception):

    def __str__(self):
        return 'You already bought this book'


class UniqueIdDoesNotMatch(Exception):

    def __str__(self):
        return 'The given unique id does not match.'


class CannotModifyOthersPeopleBookException(Exception):

    def __str__(self):
        return 'You cannot modify someone\'s book'


class BookNumberLimitReachedException(Exception):

    def __str__(self):
        return 'You have reached the maximum number of book'
