from django.urls import path
from . import views  # Ensure views are defined in authentication/views.py

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Login view
    path('register/', views.register_view, name='register'),  # Registration view
]
