from django import forms

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

class CreateRecipeForm(forms.Form):
   name = forms.CharField(max_length=120)
   cooking_time = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'In minutes'}))
   ingredients = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'List ingredients separated by commas'}))
   description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter recipe description here'}))
   pic = forms.ImageField(required=False)