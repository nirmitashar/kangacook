from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import path
from django.apps import apps
from django.views.decorators.csrf import csrf_exempt
import sys
import json

# Django settings
settings.configure(
    DEBUG=True,
    SECRET_KEY='a_random_secret_key',
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=['*'],
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.staticfiles',
        'django.contrib.auth',
        'corsheaders',
    ],
    MIDDLEWARE=[
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
    ],
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['templates'],
        },
    ],
    STATIC_URL='/static/',
    CORS_ALLOW_ALL_ORIGINS=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',  # Use in-memory database
        }
    }
)

# Initialize the Django application (required to use models)
apps.populate(settings.INSTALLED_APPS)

# Models
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    instructions = models.TextField()
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'main'

    def __str__(self):
        return self.title

# Views
def home(request):
    return render(request, 'home.html')

def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, 'recipe_list.html', {'recipes': recipes})

@csrf_exempt
def add_recipe(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        recipe = Recipe.objects.create(
            title=data['title'],
            ingredients=data['ingredients'],
            instructions=data['instructions'],
            image_url=data.get('image_url', '')
        )
        return JsonResponse({'status': 'success', 'id': recipe.id})
    return JsonResponse({'status': 'error'}, status=400)

# URL Configuration
urlpatterns = [
    path('', home, name='home'),
    path('recipes/', recipe_list, name='recipe_list'),
    path('add-recipe/', add_recipe, name='add_recipe'),
]

if __name__ == "__main__":
    # Step 1: Apply Migrations
    execute_from_command_line([sys.argv[0], 'makemigrations', 'main'])
    execute_from_command_line([sys.argv[0], 'migrate'])

    # Step 2: Start the Server
    execute_from_command_line([sys.argv[0], 'runserver'])
