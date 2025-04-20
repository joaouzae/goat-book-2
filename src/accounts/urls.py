from django.contrib.auth import views as auth_views
from django.urls import path

from accounts import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path(
        "password_reset", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path("signup", views.signup, name="signup"),
]
