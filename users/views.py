from urllib.request import HTTPRedirectHandler

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

from web_room.models import Announcement
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
    return render(request, 'users/profile.html')


@login_required
def my_ads(request):
    ads = Announcement.objects.filter(author=request.user)  # Фильтруем объявления по текущему пользователю
    return render(request, 'users/my_ads.html', {'ads': ads})


@login_required
def rent_ad(request, ad_id):
    ad = get_object_or_404(Announcement, id=ad_id)  # Получаем объявление по id
    if not ad.is_rented:  # Проверяем, не арендовано ли уже
        ad.is_rented = True  # Если не арендовано, помечаем как арендованное
        ad.renter = request.user  # Записываем текущего пользователя как арендатора
        ad.save()  # Сохраняем изменения в базе данных
    return redirect('web_room:post_detail', ad.id)  # Перенаправляем на страницу объявления





@login_required
def release_ad(request, ad_id):
    ad = get_object_or_404(Announcement, id=ad_id, author=request.user)  # Находим объявление, принадлежащее текущему пользователю
    if ad.is_rented:  # Если объявление занято
        ad.is_rented = False  # Отмечаем его как свободное
        ad.renter = None  # Убираем арендатора
        ad.save()  # Сохраняем изменения
    return redirect('users:my_ads')  # Перенаправляем пользователя обратно к списку его объявлений

