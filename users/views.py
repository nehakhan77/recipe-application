from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import CustomUser
from recipes.models import Recipe
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .forms import CustomUserCreationForm

# Create your views here.
class profile(LoginRequiredMixin, DetailView):
    model: CustomUser
    template_name = 'users/user_profile.html'
    context_object_name = 'current_user'

    def get_object(self, queryset=None):
        return CustomUser.objects.get(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch recipes authored by the current user
        context['recipes'] = Recipe.objects.filter(author=self.object)
        return context

# function to create a user
def signup_view(request):
    error_message = None
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = None
            try:
                user = User.objects.create_user(
                    username=form.cleaned_data['username']
                )
                user.set_password(form.cleaned_data['password1'])
                user.save()

                pic = form.cleaned_data['pic']
                if not pic:
                    pic = 'no_picture.jpg'

                print(user)
                print(form.cleaned_data['password1'])
                customuser = CustomUser(
                    user=user,
                    name=form.cleaned_data['name'],
                    pic=pic,
                    description=form.cleaned_data['bio'],
                    email=form.cleaned_data['email'],
                )
                customuser.save()

                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
                login(request, user)
                return redirect('users:profile')
            
            except Exception as e:
                print(e)
                if user:
                    user.delete()
                error_message = f'Something went wrong. Please try again'
        else:
            print(form.errors)
            error_message = 'Something went wrong.'
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
        'error_message': error_message
    }

    return render(request, 'auth/signup.html', context)