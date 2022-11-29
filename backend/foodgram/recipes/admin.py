from django.contrib import admin

from .models import (FavoriteRecipe, Ingredients, RecipeIngredient,
                     RecipeInShoppingCart, Recipes, Tags)

admin.site.register(FavoriteRecipe)
admin.site.register(RecipeIngredient)
admin.site.register(Tags)
admin.site.register(RecipeInShoppingCart)


class RecipeIngredientEdit(admin.TabularInline):
    model = RecipeIngredient
    extra = 0


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    list_filter = ("name",)


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ("name", "author")
    list_filter = ("author", "name", "tags")
    readonly_fields = ("recipe_in_favorite",)
    inlines = (RecipeIngredientEdit,)

    @admin.display(description="Число добавлений рецепта в избранное")
    def recipe_in_favorite(self, obj):
        return obj.user_favorite_recipes.count()
