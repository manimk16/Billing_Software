from django.shortcuts import redirect
from django.urls import reverse

def google_login(request):
    # Make sure 'somewhere' exists in your urls.py
    return redirect(reverse('somewhere'))


# google_auth/views.py
from django.shortcuts import render

def some_view(request):
    return render(request, 'template_name.html')
