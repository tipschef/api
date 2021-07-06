class UserAlreadyExistsException(Exception):
    user_email: str

    def __init__(self, user_email: str):
        self.user_email = user_email

    def __str__(self):
        return f"'{self.user_email}' already used."


class UsernameAlreadyExistsException(Exception):
    username: str

    def __init__(self, username: str):
        self.username = username

    def __str__(self):
        return f"'{self.username}' already used."


class UsernameNotFoundException(Exception):
    username: str

    def __init__(self, username: str):
        self.username = username

    def __str__(self):
        return f"User with username='{self.username}' not found."


class UserIdNotFoundException(Exception):
    user_id: int

    def __init__(self, user_id: int):
        self.user_id = user_id

    def __str__(self):
        return f"User with userid='{self.user_id}' not found."


class WrongUploadFileType(Exception):
    def __str__(self):
        return 'Upload file type must be an Image'


class UsernameNotFound(Exception):
    username: str

    def __init__(self, username: str):
        self.username = username

    def __str__(self):
        return f"'{self.username}' not found."


class EmailAlreadyExistsException(Exception):
    email: str

    def __init__(self, email: str):
        self.email = email

    def __str__(self):
        return f"'{self.email}' already used."


class UserNotPartnerException(Exception):

    def __str__(self):
        return 'User used for this request is not partner.'


class CantReachOthersDiscussionException(Exception):

    def __str__(self):
        return 'User can\'t access other user\'s discussion.'


class NotFoundDiscussionException(Exception):

    def __str__(self):
        return 'Discussion not found.'
