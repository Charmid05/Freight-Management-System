from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Django's default admin panel
    path('', include('home.urls')),  # Home routes
    path('home/', include('home.urls')),
    path('users/', include('users.urls')),
    path('shipments/', include('cargo_app.urls')),
    path('adminpanel/', include('useradmin.urls')),  # Custom admin panel
]
