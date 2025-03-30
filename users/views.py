from urllib.request import HTTPRedirectHandler

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

from web_room.forms import ReviewForm
from web_room.models import Announcement, Review
from .forms import LoginUserForm, RegisterUserForm, AnnouncementEditForm


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
    ads_list = Announcement.objects.filter(author=request.user)  # Фильтруем объявления по текущему пользователю

    paginator = Paginator(ads_list, 8)  # Ограничиваем 8 объявлениями на странице
    page_number = request.GET.get('page')  # Получаем номер текущей страницы из GET-параметров
    page_obj = paginator.get_page(page_number)  # Получаем соответствующую страницу

    return render(request, 'users/my_ads.html', {'page_obj': page_obj})


@login_required
def rent_ad(request, ad_id):
    ad = get_object_or_404(Announcement, id=ad_id)  # Получаем объявление по id
    if not ad.is_rented:  # Проверяем, не арендовано ли уже
        ad.is_rented = True  # Если не арендовано, помечаем как арендованное
        ad.renter = request.user  # Записываем текущего пользователя как арендатора
        ad.save()  # Сохраняем изменения в базе данных
    return redirect('users:ad_post_det', ad.id)  # Перенаправляем на страницу объявления





@login_required
def release_ad(request, ad_id):
    ad = get_object_or_404(Announcement, id=ad_id, author=request.user)  # Находим объявление, принадлежащее текущему пользователю
    if ad.is_rented:  # Если объявление занято
        ad.is_rented = False  # Отмечаем его как свободное
        ad.renter = None  # Убираем арендатора
        ad.save()  # Сохраняем изменения
    return redirect('users:my_ads')  # Перенаправляем пользователя обратно к списку его объявлений




@login_required
def ad_post_det(request, ad_id):
    post = get_object_or_404(Announcement, pk=ad_id)
    error = None

    if request.method == 'POST':
        if not post.is_rented:  # Проверяем, свободно ли объявление
            post.is_rented = True
            post.renter = request.user
            post.save()
            return redirect('users:ad_post_det', ad_id=post.pk)  # Возвращаем пользователя обратно
        else:
            error = 'Это объявление уже забронировано.'

    return render(request, 'users/ad_post_det.html', {'post': post, 'error': error})


def delete_ad(request, ad_id):
    ad = get_object_or_404(Announcement, id=ad_id)
    if request.user == ad.author:  # Проверяем, является ли пользователь владельцем
        ad.delete()
    return redirect('users:my_ads')  # Перенаправляем обратно на список объявлений

def remove_from_findroom(request, ad_id):
    ad = get_object_or_404(Announcement, id=ad_id)
    if request.user == ad.author:
        ad.active = False  # Предполагается, что у модели есть поле is_active
        ad.save()
    return redirect('users:my_ads')

def restore_ad(request, ad_id):
    ad = get_object_or_404(Announcement, id=ad_id)

    # Проверяем, что объявление принадлежит текущему пользователю (если нужно)
    if ad.author == request.user:
        ad.active = True  # Восстанавливаем активность
        ad.save()

    return redirect('users:my_ads')  # Перенаправляем обратно в список объявлений пользователя


def edit_ad(request, ad_id):
    # Получаем объявление по ID
    post = get_object_or_404(Announcement, pk=ad_id)

    # Если пользователь не является автором объявления, перенаправляем на страницу объявления
    if request.user != post.author:
        return redirect('users:ad_post_det', ad_id=ad_id)

    if request.method == 'POST':
        form = AnnouncementEditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()  # Сохраняем отредактированное объявление
            return redirect('users:my_ads')
    else:
        form = AnnouncementEditForm(instance=post)

    return render(request, 'users/edit_ad.html', {'form': form, 'post': post})


def rented_ads(request):
    """Отображает объявления, которые арендовал текущий пользователь."""
    rented_ads_list = Announcement.objects.filter(renter=request.user)

    return render(request, 'users/rented_ads.html', {'rented_ads': rented_ads_list})




@login_required
def cancel_rent(request, ad_id):
    """Отмена аренды объявления пользователем."""
    ad = get_object_or_404(Announcement, id=ad_id)

    if ad.renter == request.user:
        ad.renter = None  # Освобождаем аренду
        ad.is_rented = False  # Ставим статус "Свободно"
        ad.save()

    return redirect('users:rented_ads')  # Перенаправляем обратно на страницу арендованных объявлений


@login_required
def add_review(request, ad_id):
    ad = get_object_or_404(Announcement, id=ad_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.ad = ad
            review.save()
            return redirect('users:ad_post_det', ad_id=ad.id)
        else:
            print(form.errors)  # Для дебага
    else:
        form = ReviewForm()

    return render(request, 'users/ad_post_det.html', {'form': form, 'post': ad})
@login_required
def delete_review(request, review_id):
    """Удаление отзыва."""
    review = get_object_or_404(Review, id=review_id, author=request.user)
    ad_id = review.ad.id
    review.delete()
    return redirect('users:ad_post_det', ad_id=ad_id)