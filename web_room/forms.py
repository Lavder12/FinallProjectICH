from django import forms
from .models import Announcement


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

