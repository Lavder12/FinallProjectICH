from django.urls import path
from . import views

app_name = 'web_room'  # Это правильно!

urlpatterns = [
    path('find_room/', views.find_room, name='find_room'),  # Проверь, что путь правильный
    path('', views.index, name='home'),  # Главная страница
    path('register_room/', views.register_room, name='register_room'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/', views.announcement_detail, name='announcement_detail'),
]
