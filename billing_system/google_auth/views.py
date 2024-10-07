from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render


def google_login(request):
    # Make sure 'somewhere' exists in your urls.py
    return redirect(reverse('somewhere'))


# google_auth/views.py
def some_view(request):
    return render(request, 'auth/social/template_name.html')


@api_view(['GET'])
def example_view(request):
    return Response({"message": "Hello, Swagger!"})

from django.shortcuts import render

def google_login(request):
    # Handle Google login logic here
    return render(request, 'auth/google_login.html')  # Create a Google login template


def google_callback(request):
    # Your logic here
    return render(request, 'your_template.html')
