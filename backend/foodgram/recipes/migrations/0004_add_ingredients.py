# Generated by Django 3.2.16 on 2022-12-05 19:25
import csv

from django.db import migrations


with open('../../data/ingredients.csv', newline='', encoding="utf-8") as csvfile:
    ingredient_reader = csv.reader(csvfile)
    INITIAL_INGREDIENTS = [
        {'name': row[0],
         'measurement_unit': row[1]} for row in ingredient_reader
    ]


def add_ingredients(apps, schema_editor):
    Ingredients = apps.get_model('recipes', 'Ingredients')
    for ingredient in INITIAL_INGREDIENTS:
        new_tag = Ingredients(**ingredient)
        new_tag.save()


def remove_ingredients(apps, schema_editor):
    Ingredients = apps.get_model('recipes', 'Ingredients')
    for ingredient in INITIAL_INGREDIENTS:
        Ingredients.objects.get(
            name=ingredient['name'],
            measurement_unit=ingredient['measurement_unit']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_add_tags'),
    ]

    operations = [
        migrations.RunPython(
            add_ingredients,
            remove_ingredients
        )
    ]