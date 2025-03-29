from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web_room.urls')),  # Подключение маршрутов web_room
    path('users/', include('users.urls')),  # Подключение маршрутов users
]
