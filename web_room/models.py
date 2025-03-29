from django.db import models
from django.contrib.auth.models import User


class Announcement(models.Model):
    class RoomType(models.TextChoices):
        APARTMENT = "apartment", "Apartment"
        ROOM = "room", "Room"
        HOUSE = "house", "House"
        STUDIO = "studio", "Studio"

    title = models.CharField(max_length=100, verbose_name="Название")
    content = models.TextField(verbose_name="Описание")
    location = models.CharField(max_length=100, verbose_name="Местоположение")
    price = models.IntegerField(verbose_name="Цена")
    count_rooms = models.IntegerField(verbose_name="Количество комнат")

    type_of_room = models.CharField(
        max_length=10,  # Достаточно 10 символов
        choices=RoomType.choices,
        default=RoomType.APARTMENT,
        verbose_name="Выберите жильё"
    )

    active = models.BooleanField(default=True, verbose_name="Активное объявление")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    image = models.ImageField(upload_to="announcements/", blank=True, null=True, verbose_name="Фото")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", null=True, blank=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.location} ({self.get_type_of_room_display()})"
