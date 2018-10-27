"""Profile middleware"""

# Django
from django.shortcuts import redirect
from django.urls import reverse


class ProfileCompletionMiddleware:
    """Profile completion middleware.

    Ensure every user have their info.
    """

    def __init__(self, get_response):
        """Middleware initialization."""
        self.get_response = get_response

    def __call__(self, request):
        """Code to be executed for each request before the view is called."""
        if not request.user.is_anonymous:
            if not request.user.is_staff:
                profile = request.user.profile
                if not profile.picture or not profile.headline:
                    if request.path not in [reverse('profiles:update'), reverse('profiles:logout')]:
                        return redirect('profiles:update')

        response = self.get_response(request)
        return response
