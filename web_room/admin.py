from django.contrib import admin
from .models import Announcement

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price', 'count_rooms', 'type_of_room', 'is_rented', 'renter', 'created_at')  # Добавим renter
    list_filter = ('is_rented', 'type_of_room', 'created_at')
    search_fields = ('title', 'location', 'renter__username')  # Также можем искать по имени арендатора

admin.site.register(Announcement, AnnouncementAdmin)
