from django.shortcuts import render, redirect

def login_view(request):
    return render(request, 'authentication/login.html')

def register_view(request):
    # Your registration logic here
    return render(request, 'authentication/register.html')  # Adjust template path accordingly
