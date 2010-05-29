from django.contrib import admin
from rms.recipes.models import Recipe
from rms.recipes.models import Ingredient
from rms.recipes.models import Unit
from rms.recipes.models import IngredientsMap

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Unit)
admin.site.register(IngredientsMap)
