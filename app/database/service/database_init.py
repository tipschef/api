from sqlalchemy.orm import Session

from app.database.service.database import Base, engine
from app.recipe.repository.recipe.recipe_category_repository import RecipeCategoryRepository
from app.recipe.repository.recipe.recipe_cooking_type_repository import RecipeCookingTypeRepository

from app.user.model.user_model import UserModel
from app.user.model.follow_model import FollowModel
from app.user.model.subscription_model import SubscriptionModel
from app.user.model.tier_model import TierModel
from app.user.model.dashboard_model import DashboardModel

from app.recipe.model.comment_model import CommentModel
from app.recipe.model.ingredient.ingredient_model import IngredientModel
from app.recipe.model.ingredient.ingredient_unit_model import IngredientUnitModel
from app.recipe.model.like_model import LikeModel
from app.recipe.model.media.media_category_model import MediaCategoryModel
from app.recipe.model.media.media_model import MediaModel
from app.recipe.model.recipe.recipe_ingredients_model import RecipeIngredientsModel
from app.recipe.model.recipe.recipe_model import RecipeModel
from app.recipe.model.recipe.recipe_category_model import RecipeCategoryModel
from app.recipe.model.recipe.recipe_cooking_type_model import RecipeCookingTypeModel
from app.recipe.model.recipe.recipe_medias_model import RecipeMediasModel
from app.recipe.model.step.step_model import StepModel

from app.book.model.book_model import BookModel
from app.book.model.book_purchase_model import BookPurchaseModel
from app.book.model.book_recipe_model import BookRecipeModel

from app.payment.model.payment_model import PaymentModel
from app.payment.model.payslip_model import PayslipModel


def init_database() -> None:
    Base.metadata.create_all(bind=engine)


def init_data(database: Session) -> None:
    recipe_categories = ['Entrée', 'Plat principal', 'Dessert', 'Accompagnement', 'Amuse-bouche', 'Boisson', 'Confiserie', 'Sauce']
    RecipeCategoryRepository.create_recipe_categories(database, recipe_categories)

    recipe_cooking_types = ['Four', 'Plaques', 'Sans cuisson', 'Autres']
    RecipeCookingTypeRepository.create_recipe_cooking_types(database, recipe_cooking_types)