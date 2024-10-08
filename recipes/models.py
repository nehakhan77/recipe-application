from django.db import models
from users.models import CustomUser
from django.shortcuts import reverse
from django.utils import timezone

class Recipe(models.Model):
    name= models.CharField(max_length=120)
    author = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    cooking_time= models.IntegerField(default=0)
    ingredients= models.CharField(max_length=225)
    description= models.TextField(blank=True, null=True)
    _difficulty = models.CharField(max_length=120, default='')
    pic = models.ImageField(upload_to='recipes', default='no_picture.jpg')
    date_created = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
       return reverse('recipes:detail', kwargs={'pk': self.pk})

    @property
    def difficulty(self):
        if self._difficulty == '':
            self.calculate_difficulty()
        return self._difficulty
    
    def calculate_difficulty(self):
        ingredients = self.ingredients.split(", ")
        if self.cooking_time < 10 and len(ingredients) < 4:
            self._difficulty = "Easy"
        elif self.cooking_time < 10 and len(ingredients) >= 4:
            self._difficulty = "Medium"
        elif self.cooking_time >= 10 and len(ingredients) < 4:
            self._difficulty = "Intermediate"
        elif self.cooking_time >= 10 and len(ingredients) >= 4:
            self._difficulty = "Hard"