from django.urls import path
from .views import RecipeListView, RecipeDetailView
from .views import home, create_view, about_view, update_recipe, delete_recipe

app_name = 'recipes'

urlpatterns = [
   path('', home, name='home'),
   path('recipes/', RecipeListView.as_view(), name='list'),
   path('recipes/<pk>', RecipeDetailView.as_view(), name='detail'),
   path('create/', create_view, name='create'),
   path('about/', about_view, name='about'),
   path('update/<pk>/', update_recipe, name='update'),
   path('delete/<pk>/', delete_recipe, name='delete')
] 

