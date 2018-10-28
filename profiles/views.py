"""Profile views."""

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import requests

# Models
from django.contrib.auth.models import User
from profiles.models import Profile

# Forms
from profiles.forms import SignupForm



class ProfileDetailView(LoginRequiredMixin, DetailView):
    """User detail view."""

    template_name = 'profiles/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Add user's profile to context."""
        context = super().get_context_data(**kwargs)
        return context


class SignupView(FormView):
    """Users sign up view."""

    template_name = 'profiles/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('profiles:login')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update profile view."""

    template_name = 'profiles/update_profile.html'
    model = Profile
    fields = ['website', 'headline', 'phone_number', 'picture', 'torre_username']

    def get_object(self):
        """Returns User's Profile"""
        return self.request.user.profile

    def get_success_url(self):
        """Return to User's profile."""
        username = self.object.user.username
        return reverse('profiles:detail', kwargs={'username': username})


class LoginView(auth_views.LoginView):
    """Login view."""

    template_name = 'profiles/login.html'


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""

    template_name = 'profiles/logged_out.html'

@login_required
def LinkedInView(request):
    """Returns LinkedIn data"""
    if 'access_token' in request.session :
        url = 'https://api.linkedin.com/v1/people/~:(location,industry,summary,specialties,positions,public-profile-url,num-connections,picture-url)?format=json'
        headers = {'Authorization': 'Bearer ' + request.session['access_token']}
        response = requests.get(url, headers=headers)
        content = response.json()
    else:
        content = 'No data'
    
    return render(request, 'profiles/linkedin.html', {'data': content})

@login_required
def TorreBioView(request):
    """Returns Torre Bio data"""

    torre_username = request.user.profile.torre_username
    url = 'https://torre.bio/api/people/' + torre_username
    
    
    response = requests.get(url)
    content = response.json()
    return render(request, 'profiles/torrebio.html', {'data': content})

@login_required
def MergeView(request):
    """Returns LinkedIn and Torre Bio data"""

    torre_username = request.user.profile.torre_username
    url = 'https://torre.bio/api/people/' + torre_username
    
    
    response = requests.get(url)
    content = response.json()
    return render(request, 'profiles/merged.html', {'data': content})