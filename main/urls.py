from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Добавляем маршруты для пользователей
    path('web_room/', include('web_room.urls')),  # Маршруты для web_room
    path('', include('web_room.urls')),
]
if settings.DEBUG:  # Только для разработки
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
