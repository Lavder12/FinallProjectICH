from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from web_room import views as vi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vi.index, name='home'),
    path('register_room/', vi.register_room, name='register_room'),
    path('find_room/', vi.find_room, name='find_room'),
    path('users/', include('users.urls')),
    path('post/<int:pk>/',vi.post_detail, name='post_detail'),# namespace теперь работает благодаря app_name в users/urls.py
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)