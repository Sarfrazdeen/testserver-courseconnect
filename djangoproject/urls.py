from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
secure_admin = login_required(admin.site.urls)

urlpatterns = [
    
    path('secure-admin/', secure_admin),

    # Route requests to backend app
    path('', include('backend.urls')),

    # Route authentication URLs (login functionality)
    path('auth/', include('Authentication.urls')), 

    path('tasks/', include('tasks.urls')),
]

# Serve static files during development when DEBUG is True
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)