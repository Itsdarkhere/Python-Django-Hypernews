from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('news', include('news/urls')),
    path('', include('news/urls')),
]

urlpatterns += static(settings.STATIC_URL)