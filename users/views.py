from urllib.request import HTTPRedirectHandler

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy

from web_room.models import Announcement, Reservation
from .forms import LoginUserForm, RegisterUserForm


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return render(request, 'users/register_done.html')
    else:
        form = RegisterUserForm()
    return render(request, 'users/register.html', {'form': form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))


@login_required
def profile_view(request):
    # Сдаваемые объявления пользователя
    my_announcements = Announcement.objects.filter(author=request.user)  # Объявления текущего пользователя

    # Арендованные объекты
    rented_announcements = Reservation.objects.filter(user=request.user).select_related('announcement')

    return render(request, 'users/profile.html', {
        'my_announcements': my_announcements,
        'rented_announcements': [r.announcement for r in rented_announcements],  # Арендованные объявления
    })
