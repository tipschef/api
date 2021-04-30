from app.database.service.database import Base, engine

from app.user.model.user_model import UserModel
from app.user.model.follow_model import FollowModel
from app.user.model.subscription_model import SubscriptionModel

from app.recipe.model.comment_model import CommentModel
from app.recipe.model.ingredient_model import IngredientModel
from app.recipe.model.ingredient_unit_model import IngredientUnitModel
from app.recipe.model.like_model import LikeModel
from app.recipe.model.media_category_model import MediaCategoryModel
from app.recipe.model.media_model import MediaModel
from app.recipe.model.recipe_ingredients_model import RecipeIngredientsModel
from app.recipe.model.recipe_model import RecipeModel
from app.recipe.model.recipe_pictures_model import RecipePicturesModel

from app.book.model.book_model import BookModel
from app.book.model.book_purchase_model import BookPurchaseModel
from app.book.model.book_recipe_model import BookRecipeModel


def init_database() -> None:
    Base.metadata.create_all(bind=engine)
