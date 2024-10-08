from django import forms
from .models import Recipe
from django.forms import TextInput, Textarea, NumberInput

CHART__CHOICES = (
   ('bar_chart', 'Bar chart'),
   ('pie_chart', 'Pie chart'),
   ('line_chart', 'Line Chart'),
)

class RecipeSearchForm(forms.Form): 
   recipe_name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search for an ingredient or recipe name here',
        })
    )
   chart_type = forms.ChoiceField(choices=CHART__CHOICES)

class CreateRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [ "name", "cooking_time", "ingredients", "description", "pic"]
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'cooking_time': forms.NumberInput(attrs={'class': 'form-control', }),
            'ingredients': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Separate each ingredient with a comma'}),
            'description': Textarea(attrs={'class': 'form-control'}),
        }