from django.urls import path
from . import views
from .views import example_view

urlpatterns = [
    path('login/', views.google_login, name='google_login'),
    path('somewhere/', views.some_view, name='somewhere'),

    path('example/', example_view, name='example-view'),
]