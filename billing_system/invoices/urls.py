from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.shortcuts import render

# Import your ViewSets and PayPal-related views
from invoices.views import ClientViewSet, InvoiceViewSet, PaymentViewSet  # Assuming these are defined in invoices/views.py
#from payment.views import create_payment, payment_success, payment_cancel, execute_payment  # Assuming these are in payment/views.py

# Setting up DRF router for ViewSets
router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'payments', PaymentViewSet)

# Setting up schema view for Swagger documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Billing System API",
        default_version='v1',
        description="API for Billing System with Google OAuth",
        contact=openapi.Contact(email="contact@yourapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Home view for the root URL
def home_view(request):
    return render(request, 'auth/social/home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),  # Home view for root URL
    path('google-auth/', include('google_auth.urls')),
    path('', include(router.urls)),

    # Authentication URLs
    path('auth/', include('social_django.urls', namespace='social_auth')),  # Social authentication
    path('accounts/', include('allauth.urls')),  # Allauth routes for authentication
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Login view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout view

    # JWT Token Authentication URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Token obtain
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),  # Token blacklist

    # API Router
    path('api/', include(router.urls)),  # Using DRF router for ViewSets

    # App URLs
    path('invoices/', include('invoices.urls')),  # URLs for invoice management
    path('auth/social/custom/', include('google_auth.urls')),  # Custom social login/register

    # Swagger API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Payment PayPal
    """path('payment/create/', create_payment, name='create_payment'),
    path('payment/success/', payment_success, name='payment_success'),
    path('payment/cancel/', payment_cancel, name='payment_cancel'),
    path('payment/execute/', execute_payment, name='execute_payment'),"""
]
from django.urls import path
from . import views  # Ensure views are defined in invoices/views.py

urlpatterns = [
    path('', views.InvoiceListView.as_view(), name='invoice_list'),  # Example for listing invoices
    path('<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),  # Example for viewing a specific invoice
    # Add additional invoice-related URLs as needed
]
