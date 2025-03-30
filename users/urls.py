from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('my_ads/', views.my_ads, name='my_ads'),
    path('rent-ad/<int:ad_id>/', views.rent_ad, name='rent_ad'),
    path('release-ad/<int:ad_id>/', views.release_ad, name='release_ad'),

]
