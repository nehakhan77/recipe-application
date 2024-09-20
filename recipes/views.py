from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Recipe, CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import RecipeSearchForm, CreateRecipeForm
import pandas as pd
from .utils import get_recipename_from_id, get_chart
from django.db.models import Q

def home(request):
   return render(request, 'recipes/recipes_home.html')

class RecipeListView(LoginRequiredMixin,ListView): #class-based view
   model = Recipe                                  #specify model
   
   def get(self, request):
      form = RecipeSearchForm(request.POST or None)
      recipes = Recipe.objects.all()
      return render(request, 'recipes/recipes_list.html', {'form': form, 'recipes': recipes})
   
   def post(self, request):
      form = RecipeSearchForm(request.POST or None)
      recipes = Recipe.objects.all()
      chart = None

      if request.method =='POST':
       recipe_name = request.POST.get('recipe_name')
       chart_type = request.POST.get('chart_type')
       print (recipe_name, chart_type)

      qs = Recipe.objects.filter(Q(name__icontains=recipe_name) | Q(ingredients__icontains=recipe_name))
      if qs.exists():     
         recipes=pd.DataFrame(qs.values()) 
         recipes['difficulty'] = recipes.apply(lambda row: get_recipename_from_id(row['id']).difficulty, axis=1)
         chart=get_chart(chart_type, recipes, labels=recipes['id'].values)
      else:
         recipes = pd.DataFrame()
         

      context = {
            'form': form,
            'recipes': recipes,
            'chart': chart,
      }
      
      return render(request, 'recipes/recipes_list.html', context)

class RecipeDetailView(LoginRequiredMixin,DetailView):  #class-based view
   model = Recipe                                       #specify model
   template_name = 'recipes/recipes_detail.html'        #specify template

@login_required
def create_view(request):
      create_form = CreateRecipeForm(request.POST or None, request.FILES or None)

      if request.method == 'POST' and create_form.is_valid():
         name = create_form.cleaned_data.get('name')
         cooking_time = create_form.cleaned_data.get('cooking_time')
         ingredients = create_form.cleaned_data.get('ingredients')
         pic = create_form.cleaned_data.get('pic')  # Retrieve the uploaded image
         description = create_form.cleaned_data.get('description')

         custom_user = CustomUser.objects.get(user=request.user)

         recipe = Recipe.objects.create(
            name=name,
            cooking_time=cooking_time,
            ingredients=ingredients,
            description=description,
            pic=pic, # Save the image to the recipe
            author=custom_user  # Set the current user as the author
         )
         
         return redirect(recipe.get_absolute_url())  # Redirect after saving

      context = {
         'create_form': create_form
      }

      return render(request, 'recipes/recipes_create.html', context)

def about_view(request):
   return render(request, 'recipes/recipes_about.html')