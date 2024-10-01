from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.google_login, name='google_login'),
    path('somewhere/', views.some_view, name='somewhere'),
]
