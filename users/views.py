from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as AuthLoginView # Avoid naming conflict
from django.contrib.auth.views import LogoutView as AuthLogoutView # Avoid naming conflict
from .forms import SignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log the user in immediately after signup
            return redirect('home') # Redirect to home page
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Use built-in LoginView and LogoutView, just define them here for clarity
# We will reference them by name in urls.py
# You can customize them further if needed by subclassing
class LoginView(AuthLoginView):
    template_name = 'registration/login.html'

class LogoutView(AuthLogoutView):
    # No template needed by default, redirects to LOGOUT_REDIRECT_URL
    pass