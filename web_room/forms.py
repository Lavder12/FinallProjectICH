from django import forms
from .models import Announcement, Reservation


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "content", "location", "price", "count_rooms", "type_of_room", "image"]

        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "count_rooms": forms.NumberInput(attrs={"class": "form-control"}),
            "type_of_room": forms.Select(attrs={"class": "custom-select"}),
        }




class SearchRoomForm(forms.Form):
    ROOM_TYPES = [
        ('', 'Тип комнаты'),
        ('apartment', 'Apartment'),
        ('room', 'Room'),
        ('house', 'House'),
        ('studio', 'Studio'),
    ]

    type = forms.ChoiceField(choices=ROOM_TYPES, required=False, widget=forms.Select(attrs={'class': 'search-input'}), label='')
    location = forms.CharField(max_length=100, required=False,
                               widget=forms.TextInput(attrs={'class': 'search-input', 'placeholder': 'Местоположение'}), label='')
    min_price = forms.IntegerField(required=False, widget=forms.NumberInput(
        attrs={'class': 'search-input', 'placeholder': 'Минимальная цена'}), label='')
    max_price = forms.IntegerField(required=False, widget=forms.NumberInput(
        attrs={'class': 'search-input', 'placeholder': 'Максимальная цена'}), label='')
    rooms = forms.CharField(max_length=50, required=False,
                            widget=forms.TextInput(attrs={'class': 'search-input', 'placeholder': 'Количество комнат'}), label='')
    q = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'search-input', 'placeholder': 'Поиск '}), label='')

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
