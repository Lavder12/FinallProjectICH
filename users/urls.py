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
    path('ad_post/<int:ad_id>/', views.ad_post_det, name='ad_post_det'),
    path('ad_delete/<int:ad_id>/', views.delete_ad, name='delete_ad'),
    path('ad_remove_findroom/<int:ad_id>/', views.remove_from_findroom, name='remove_from_findroom'),
    path('ad_restore/<int:ad_id>/', views.restore_ad, name='restore_ad'),
    path('edit_ad/<int:ad_id>/', views.edit_ad, name='edit_ad'),
    path('rented_ads/', views.rented_ads, name='rented_ads'),
    path('cancel_rent/<int:ad_id>/', views.cancel_rent, name='cancel_rent'),
    path('ad/<int:ad_id>/review/', views.add_review, name='add_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),

]
