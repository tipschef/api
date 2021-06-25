class RecipeIdNotFoundException(Exception):

    def __str__(self):
        return 'The given recipe ID cannot be found'


class CannotModifyOthersPeopleRecipeException(Exception):

    def __str__(self):
        return 'You cannot modify someone\'s recipe'


class NotRecipeOwnerException(Exception):
    def __str__(self):
        return 'You are not the recip\'s owner'


class UserNotAuthorized(Exception):
    min_tier: int

    def __init__(self, min_tier: int):
        self.min_tier = min_tier

    def __str__(self):
        return 'You are not authorized to see this recipe'

    def as_dict(self):
        return {
            'detail': str(self),
            'min_tier': self.min_tier
        }


class WrongUserToDeleteComment(Exception):
    comment_id: int

    def __init__(self, comment_id: int):
        self.comment_id = comment_id

    def __str__(self):
        return f'You are not the owner of this comment `{self.comment_id}`'
