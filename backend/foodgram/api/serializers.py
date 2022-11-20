import base64

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from recipes.models import (FavoriteRecipe, Ingredients, RecipeIngredient,
                            RecipeInShoppingCart, Recipes, RecipeTag, Tags)
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import Subscription
from users.validators import UsernameValidator

User = get_user_model()


class CustomUsersSerializer(UserSerializer):
    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LENGTH,
        validators=(UniqueValidator(queryset=User.objects.all()),
                    UsernameValidator(),)
    )
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("username", "id", "email", "first_name",
                  "last_name", "is_subscribed", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return Subscription.objects.filter(
            user=user, author=obj).exists()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ("id", "name", "color", "slug")


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ("id", "name", "measurement_unit")


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)
        return super().to_internal_value(data)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all(),
        source="ingredient.id"
    )
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUsersSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(source="recipeingredient_set",
                                             many=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = ("id", "tags", "author", "ingredients", "is_favorited",
                  "is_in_shopping_cart", "name", "image", "text",
                  "cooking_time")

    def get_is_favorited(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return FavoriteRecipe.objects.filter(
            recipe=obj, user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return RecipeInShoppingCart.objects.filter(
            recipe=obj, user=user).exists()

    def create(self, validated_data):
        validated_data.pop("recipeingredient_set")
        context_request = self.context["request"]
        ingredients = context_request.data["ingredients"]
        tags_id = context_request.data["tags"]
        recipe = Recipes.objects.create(**validated_data,
                                        author=context_request.user)
        for id in tags_id:
            tag = get_object_or_404(Tags, id=id)
            RecipeTag.objects.create(recipe=recipe, tag=tag)
        for ingredient_dict in ingredients:
            ingredient = get_object_or_404(Ingredients,
                                           id=ingredient_dict.get("id"))
            amount = ingredient_dict.get("amount")
            RecipeIngredient.objects.create(recipe=recipe,
                                            ingredient=ingredient,
                                            amount=amount)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get("image", instance.image)
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get("cooking_time",
                                                   instance.cooking_time)
        tag_list = self.context["request"].data.get("tags")
        if tag_list:
            instance.tags.set(tag_list)
        if "recipeingredient_set" in validated_data:
            RecipeIngredient.objects.filter(recipe=instance).delete()
            validated_data.pop("recipeingredient_set")
            context_request = self.context["request"]
            ingredients = context_request.data["ingredients"]
            for ingredient_dict in ingredients:
                ingredient = get_object_or_404(Ingredients,
                                               id=ingredient_dict.get("id"))
                amount = ingredient_dict.get("amount")
                RecipeIngredient.objects.get_or_create(recipe=instance,
                                                       ingredient=ingredient,
                                                       amount=amount)
        instance.save()
        return instance


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ("id", "name", "image", "cooking_time")


class SubscriptionSerializer(CustomUsersSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(CustomUsersSerializer.Meta):
        fields = (CustomUsersSerializer.Meta.fields
                  + ("recipes", "recipes_count",))

    def get_recipes(self, obj):
        return ShortRecipeSerializer(obj.recipes.all(), many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()
