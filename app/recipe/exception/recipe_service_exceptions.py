class RecipeIdNotFoundException(Exception):

    def __str__(self):
        return 'The given recipe ID cannot be found'


class CannotModifyOthersPeopleRecipeException(Exception):

    def __str__(self):
        return 'You cannot modify someone\'s recipe'


class NotRecipeOwnerException(Exception):
    def __str__(self):
        return 'You are not the recip\'s owner'
