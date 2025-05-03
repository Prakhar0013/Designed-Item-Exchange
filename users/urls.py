from django.urls import path
from . import views

# No app_name needed if using named URLs directly in templates

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    # Use Django's built-in views by name or our custom subclasses
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # Add paths for password reset, change etc. later if needed
    # path('password_reset/', ..., name='password_reset'),
]