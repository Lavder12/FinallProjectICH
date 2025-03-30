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
        max_length=10,
        choices=RoomType.choices,
        default=RoomType.APARTMENT,
        verbose_name="Выберите жильё"
    )

    active = models.BooleanField(default=True, verbose_name="Активное объявление")
    is_rented = models.BooleanField(default=False, verbose_name="Забронировано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    image = models.ImageField(upload_to="announcements/", blank=True, null=True, verbose_name="Фото")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор",
                               related_name="created_announcements")

    renter = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Арендатор"
    )

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]

    def __str__(self):
        status = "Забронировано" if self.is_rented else "Свободно"
        return f"{self.title} - {self.location} ({self.get_type_of_room_display()}) | {status}"


from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    ad = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, f"{i}⭐") for i in range(1, 6)], null=False, blank=False)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('ad', 'author')  # Один пользователь - один отзыв

    def __str__(self):
        return f"Отзыв {self.author} - {self.rating}⭐"
