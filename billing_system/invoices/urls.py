from django.urls import path
from . import views
from .views import client_list, invoice_list, payment_list, client_detail
from .views import GoogleLoginCallback

urlpatterns = [
    path('clients/', client_list, name='client-list'),
    path('clients/<int:id>/', client_detail, name='client-detail'), 
    path('invoices/', invoice_list, name='invoice_list'),
    path('payments/', payment_list, name='payment_list'),
    path('login/', GoogleLoginCallback.as_view(), name='google-login'),
]
