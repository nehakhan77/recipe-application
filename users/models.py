from django.db import models
from django.contrib.auth.models import User #needed for OneToOneField

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name= models.CharField(max_length=120)
    email = models.EmailField(default='example@example.com')
    pic = models.ImageField(upload_to='users', default='no_picture.jpg')
    description= models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name)
