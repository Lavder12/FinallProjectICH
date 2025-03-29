# models.py

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


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
    is_rented = models.BooleanField(default=False, verbose_name="Забронировано")  # Добавлено новое поле
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    image = models.ImageField(upload_to="announcements/", blank=True, null=True, verbose_name="Фото")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", null=True, blank=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.location} ({self.get_type_of_room_display()})"


class Reservation(models.Model):
    announcement = models.ForeignKey(Announcement, related_name="reservations", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(verbose_name="Дата начала")
    end_date = models.DateTimeField(verbose_name="Дата окончания")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания бронирования")

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Reservation by {self.user.username} for {self.announcement.title} from {self.start_date} to {self.end_date}"

    def is_conflicting(self):
        """Проверяет, существует ли пересечение с другими бронированиями."""
        conflicting_reservations = Reservation.objects.filter(
            announcement=self.announcement,
            end_date__gt=self.start_date,
            start_date__lt=self.end_date
        )
        return conflicting_reservations.exists()
