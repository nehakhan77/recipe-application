from django.test import TestCase
from .models import Recipe 
from users.models import User
from .forms import RecipeSearchForm


class MyTestClass(TestCase):
   def setUpTestData():
      # Set up non-modified objects used by all test methods
      Recipe.objects.create(name='Ravoili', cooking_time='10', ingredients='ravioli, sauce, cheese', description='this is a traditional Italian dish')

   def test_recipe_name(self):
      # Get a recipe object to test
      recipe = Recipe.objects.get(id=1)

      # Get the metadata for the 'name' field and use it to query its data
      field_label = recipe._meta.get_field('name').verbose_name

      # Compare the value to the expected result
      self.assertEqual(field_label, 'name')

   def test_ingredients_max_length(self):
         # Get a recipe object to test
         recipe = Recipe.objects.get(id=1)
         # Get the metadata for the 'ingredients' field and use it to query its max_length
         max_length = recipe._meta.get_field('ingredients').max_length
         # Compare the value to the expected result
         self.assertEqual(max_length, 225)

   def test_cooking_time_is_integer(self):
      recipe = Recipe.objects.get(id=1)
      cooking_time = recipe.cooking_time
      self.assertIs(type(cooking_time), int, 'cooking_time is not a number')

   def test_recipe_description(self):
      recipe = Recipe.objects.get(id=1)
      field_label = recipe._meta.get_field('description').verbose_name
      self.assertEqual(field_label, 'description')

   def test_get_absolute_url(self):
      recipe = Recipe.objects.get(id=1)
      #get_absolute_url() should take you to the detail page of book #1
      #and load the URL /books/list/1
      self.assertEqual(recipe.get_absolute_url(), '/recipes/1')

   def test_calculate_difficulty(self):
      recipe = Recipe(cooking_time=20, ingredients="Ingredient 1, Ingredient 2, Ingredient 3, Ingredient 4, Ingredient 5")
      self.assertEqual(recipe.difficulty, "Hard")

   def test_recipe_pic(self):
      recipe = Recipe.objects.get(id=1)
      self.assertEqual(recipe.pic, 'no_picture.jpg')


class RecipeFormsTest(TestCase):
    def setUpTestData():
        user = User.objects.create_user(username='testuser', password='testpassword')
        Recipe.objects.create(
            name='Test Recipe',
            cooking_time=30,
            ingredients='Ingredient 1, Ingredient 2',
            pic='test_pic.jpg',
            description="description",
            author=user
        )
    
    def test_recipes_search_form(self):
        form_data = {'recipe_name': 'Chai', 'chart_type': 'bar_chart'}
        form = RecipeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

   
