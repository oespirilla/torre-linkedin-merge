"""Users views."""

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView

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
    fields = ['website', 'headline', 'phone_number', 'picture']

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
