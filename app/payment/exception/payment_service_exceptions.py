class UserNotCookException(Exception):

    def __str__(self):
        return "The current user isn't a verified `cook`"


class NoAccountIdException(Exception):

    def __str__(self):
        return "The current used has no account_id"


class NoPaymentMethodException(Exception):

    def __str__(self):
        return "The user does not have payment method"
