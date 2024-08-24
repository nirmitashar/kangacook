from django.urls import path
from . import views

urlpatterns = [
    path('recipes/', views.recipe_list, name='api_recipe_list'),  # GET: View all recipes
    path('add-recipe/', views.add_recipe, name='api_add_recipe'),  # POST: Add a new recipe
]

