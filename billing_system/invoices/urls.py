from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.shortcuts import render
from invoices.views import ClientViewSet, InvoiceViewSet, PaymentViewSet
from . import views

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

    # Google auth and social auth
    path('google-auth/', include('google_auth.urls')),  # Google OAuth
    path('auth/', include('social_django.urls', namespace='social_auth')),  # Social authentication
    path('accounts/', include('allauth.urls')),  # Allauth routes for authentication

    # JWT Token Authentication URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # DRF router
    path('', include(router.urls)),

    # Swagger API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Invoice-specific routes
    path('list/', views.invoice_list, name='invoice_list'),
    path('create/', views.invoice_create, name='invoice_create'),
    path('<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),  # View specific invoice
    path('invoice/<int:invoice_id>/', views.fetch_invoice, name='fetch_invoice'),  # Fetch specific invoice data
    path('invoice/<int:invoice_id>/download/', views.download_invoice, name='download_invoice'),  # Download invoice
]
