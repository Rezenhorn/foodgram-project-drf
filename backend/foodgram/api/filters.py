from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipes, Tags


class RecipeFilter(FilterSet):
    author = filters.CharFilter()
    is_in_shopping_cart = filters.BooleanFilter(
        field_name="is_in_shopping_cart",
        method="filter"
    )
    is_favorited = filters.BooleanFilter(field_name="is_favorited",
                                         method="filter")
    tags = filters.ModelMultipleChoiceFilter(queryset=Tags.objects.all(),
                                             field_name="tags__slug",
                                             to_field_name="slug")

    class Meta:
        model = Recipes
        fields = ("author", "tags", "is_favorited", "is_in_shopping_cart")

    def filter(self, queryset, name, value):
        user = self.request.user
        if name == "is_in_shopping_cart" and value:
            return queryset.filter(cart_recipe__user=user)
        if name == "is_favorited" and value:
            return queryset.filter(fav_recipe__user=user)
        return queryset
