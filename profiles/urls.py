"""Profile URLs."""

# Django
from django.urls import path

# View
from profiles import views


urlpatterns = [

    # Management
    path(
        route='login/',
        view=views.LoginView.as_view(),
        name='login'
    ),
    path(
        route='logout/',
        view=views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        route='signup/',
        view=views.SignupView.as_view(),
        name='signup'
    ),
    path(
        route='me/',
        view=views.UpdateProfileView.as_view(),
        name='update'
    ),
    path(
        route='<str:username>/',
        view=views.ProfileDetailView.as_view(),
        name='detail'
    )

]
