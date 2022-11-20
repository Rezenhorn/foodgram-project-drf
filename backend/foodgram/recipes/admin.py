from django.contrib import admin

from .models import (FavoriteRecipe, Ingredients, RecipeIngredient,
                     RecipeInShoppingCart, Recipes, RecipeTag, Tags)

admin.site.register(FavoriteRecipe)
admin.site.register(RecipeIngredient)
admin.site.register(Tags)
admin.site.register(RecipeTag)
admin.site.register(RecipeInShoppingCart)


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    list_filter = ("name",)


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ("name", "author")
    list_filter = ("author", "name", "tags")
    readonly_fields = ("recipe_in_favorite",)

    @admin.display(description="Число добавлений рецепта в избранное")
    def recipe_in_favorite(self, obj):
        return obj.fav_recipe.count()
