from django.urls import path
from .views import profile, signup_view

app_name = 'users'

urlpatterns = [
  path("profile/", profile.as_view(), name="profile"),
  path("signup/", signup_view, name="signup" )
]