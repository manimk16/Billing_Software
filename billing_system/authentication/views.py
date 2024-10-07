from django.shortcuts import render, redirect
from django.contrib.auth import logout

def login_view(request):
    return render(request, 'authentication/login.html')

def register_view(request):
    # Your registration logic here
    return render(request, 'authentication/register.html')  # Adjust template path accordingly

def logout_view(request):
    logout(request)  # This logs out the user
    return redirect('login')  # Redirect to the login page after logout
