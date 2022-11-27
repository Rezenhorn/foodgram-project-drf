from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from .validators import ColorHexValidator, TagSlugValidator

User = get_user_model()


class Tags(models.Model):
    name = models.CharField("Название", max_length=200, unique=True)
    color = models.CharField("Цвет",
                             max_length=7,
                             unique=True,
                             validators=(ColorHexValidator,))
    slug = models.SlugField("Слаг",
                            max_length=200,
                            unique=True,
                            validators=(TagSlugValidator,))

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.CharField("Название", max_length=200)
    measurement_unit = models.CharField("Единицы измерения",
                                        max_length=200)

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Recipes(models.Model):
    author = models.ForeignKey(User,
                               verbose_name="Автор",
                               on_delete=models.CASCADE,
                               related_name="recipes")
    name = models.CharField("Название", max_length=200, unique=True)
    text = models.TextField("Описание")
    cooking_time = models.PositiveIntegerField(
        "Время приготовления",
        validators=(MinValueValidator(
            1, message="Минимальное время приготовления 1 минута."),)
    )
    image = models.ImageField("Картинка",
                              upload_to="foodgram/images/",
                              default=None)
    tags = models.ManyToManyField(Tags,
                                  verbose_name="Теги",
                                  through="RecipeTag")
    pub_date = models.DateTimeField("Дата публикации",
                                    auto_now_add=True,
                                    db_index=True)

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipes,
                               verbose_name="Рецепт",
                               on_delete=models.CASCADE,
                               related_name="ingredients")
    ingredient = models.ForeignKey(Ingredients,
                                   verbose_name="Ингредиент",
                                   on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        "Количество",
        validators=(MinValueValidator(
            1, message="Минимальное количество ингредиента равно 1."),)
    )

    class Meta:
        verbose_name = "Ингредиент для рецепта"
        verbose_name_plural = "Ингредиенты для рецепта"
        constraints = [
            models.UniqueConstraint(fields=["recipe", "ingredient"],
                                    name="unique_ingredient")
        ]

    def __str__(self):
        return (f"{self.recipe}: {self.ingredient} {self.amount} "
                f"{self.ingredient.measurement_unit}")


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags,
                            on_delete=models.CASCADE,
                            related_name="recipe_tag")

    class Meta:
        verbose_name = "Тег рецепта"
        verbose_name_plural = "Теги рецепта"
        constraints = [
            models.UniqueConstraint(fields=["recipe", "tag"],
                                    name="unique_tag")
        ]

    def __str__(self):
        return (f"{self.recipe}: {self.tag}")


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User,
                             verbose_name="Пользователь",
                             on_delete=models.CASCADE,
                             related_name="favorite_recipes")
    recipe = models.ForeignKey(Recipes,
                               verbose_name="Рецепт",
                               on_delete=models.CASCADE,
                               related_name="user_favorite_recipes")

    class Meta:
        verbose_name = "Рецепт в избранном"
        verbose_name_plural = "Рецепты в избранном"
        constraints = [models.UniqueConstraint(fields=["user", "recipe"],
                                               name="unique_favorite")]

    def __str__(self):
        return (f"{self.user}: {self.recipe}")


class RecipeInShoppingCart(models.Model):
    user = models.ForeignKey(User,
                             verbose_name="Пользователь",
                             on_delete=models.CASCADE,
                             related_name="cart_user")
    recipe = models.ForeignKey(Recipes,
                               verbose_name="Рецепт",
                               on_delete=models.CASCADE,
                               related_name="cart_recipe")

    class Meta:
        verbose_name = "Рецепт в корзине"
        verbose_name_plural = "Рецепты в корзине"
        constraints = [models.UniqueConstraint(fields=["user", "recipe"],
                                               name="unique_shopping_cart")]

    def __str__(self):
        return (f"{self.user}: {self.recipe}")
