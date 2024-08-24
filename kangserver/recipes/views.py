from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Recipe
import json

# API to view all recipes
def recipe_list(request):
    if request.method == 'GET':
        recipes = Recipe.objects.all().order_by('-created_at')
        recipes_data = []
        for recipe in recipes:
            recipes_data.append({
                'id': recipe.id,
                'title': recipe.title,
                'ingredients': recipe.ingredients,
                'instructions': recipe.instructions,
                'image_url': recipe.image_url,
                'created_at': recipe.created_at,
            })
        print(recipes_data)
        return JsonResponse({'recipes': recipes_data})

# API to add a new recipe
@csrf_exempt
def add_recipe(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            recipe = Recipe.objects.create(
                title=data['title'],
                ingredients=data['ingredients'],
                instructions=data['instructions'],
                image_url=data.get('image_url', '')
            )
            return JsonResponse({'status': 'success', 'id': recipe.id}, status=201)
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
