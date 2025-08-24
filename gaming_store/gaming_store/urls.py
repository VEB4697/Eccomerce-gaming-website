# gaming_store/urls.py (or your project's main urls.py)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Link the root URL to your 'page' app
    path('', include('page.urls')),
    # Link the '/games/' URLs to your 'games' app
    path('games/', include('games.urls')),
    # This is the new line you need to add
    path('users/', include('users.urls')),
    
]

# This is for serving media files (like game images) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
