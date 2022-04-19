from django.urls import path, include


urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('core/', include('Core.urls')),
    path('payroll/', include('Payroll.urls')),
    path('lookup/', include('Lookup.urls')),
    path('contact/', include('Contact.urls')),
    path('sales/', include('Sales.urls')),
]
