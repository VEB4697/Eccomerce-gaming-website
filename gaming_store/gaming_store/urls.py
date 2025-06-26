from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(('users.urls', 'users'))),  # 👈 Namespace is 'users'
    path('page/', include(('page.urls', 'page'))), # Ensure this includes login and register views
    path('', lambda request: redirect('users:login')),  # Redirect to login page by name
    path('', lambda request: redirect('users:register')),  # Redirect to login page by name
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)