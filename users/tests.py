from django.test import TestCase
from .models import CustomUser
from users.models import User
from django.contrib.auth.models import User

class MyTestClass(TestCase):
    def setUpTestData():
       user = User.objects.create_user(username='maxmustermann', password='testpassword')
       CustomUser.objects.create(user=user, name='Max Mustermann', description='Hi, I am Max Mustermann.')

    def test_user_name_max_length(self):
        user = CustomUser.objects.get(id=1)
        max_length = user._meta.get_field('name').max_length
        self.assertEqual(max_length, 120)


    def test_user_username_max_length(self):
        user = CustomUser.objects.get(id=1)
        max_length = user.user._meta.get_field('username').max_length
        self.assertEqual(max_length, 150, 'username has over 120 characters')

    def test_user_bio(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_users_pic(self):
        user = CustomUser.objects.get(id=1)
        self.assertEqual(user.pic, 'no_picture.jpg')



       
