from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.google_login, name='google_login'),
]
