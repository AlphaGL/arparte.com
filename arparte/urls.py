"""
ARPARTE Main URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('marketplace.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler404 = 'marketplace.views.error_404'
handler403 = 'marketplace.views.error_403'
handler500 = 'marketplace.views.error_500'
handler400 = 'marketplace.views.error_400'

# Customize admin site
admin.site.site_header = "ARPARTE Administration"
admin.site.site_title = "ARPARTE Admin"
admin.site.index_title = "Welcome to ARPARTE Admin Panel"