from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AnnouncementForm, SearchRoomForm
from .models import Announcement


# Главная страница
def index(request):
    return render(request, 'web_room/main_page.html')


# Поиск комнаты
def find_room(request):
    form = SearchRoomForm(request.GET)
    posts = Announcement.objects.filter(is_rented=False, active=True)  # Фильтрация только доступных и активных объявлений

    # Применяем фильтры, если форма валидна
    if form.is_valid():
        search_query = form.cleaned_data.get('q')
        location_query = form.cleaned_data.get('location')
        min_price_query = form.cleaned_data.get('min_price')
        max_price_query = form.cleaned_data.get('max_price')
        rooms_query = form.cleaned_data.get('rooms')
        type_query = form.cleaned_data.get('type')

        if search_query:
            posts = posts.filter(title__icontains=search_query) | posts.filter(content__icontains=search_query)
        if location_query:
            posts = posts.filter(location__icontains=location_query)
        if min_price_query:
            posts = posts.filter(price__gte=min_price_query)
        if max_price_query:
            posts = posts.filter(price__lte=max_price_query)
        if rooms_query:
            posts = posts.filter(count_rooms=rooms_query)
        if type_query:
            posts = posts.filter(type_of_room__icontains=type_query)

    # Обработка сортировки
    sort = request.GET.get("sort", "date_desc")
    sort_mapping = {
        "rating_asc": "rating",
        "rating_desc": "-rating",
        "date_asc": "created_at",
        "date_desc": "-created_at",
        "price_asc": "price",
        "price_desc": "-price",
    }
    posts = posts.order_by(sort_mapping.get(sort, "-created_at"))

    # Пагинация (по 5 объявлений на страницу)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Рендер результата
    return render(request, "web_room/find_room.html", {
        "form": form,
        "page_obj": page_obj,
        "sort": sort,
    })


# Регистрация нового объявления (только для авторизованных пользователей)
@login_required
def register_room(request):
    if request.method == "POST":
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user  # Добавляем автора из модели User
            announcement.save()
            return redirect('web_room:home')  # Перенаправляем на главную страницу
    else:
        form = AnnouncementForm()  # Пустая форма для GET-запросов
    return render(request, "web_room/register_room.html", {"form": form})


# Детали поста с обработкой аренды
def post_detail(request, pk):
    post = get_object_or_404(Announcement, pk=pk)

    if request.method == 'POST':
        if not post.is_rented:  # Проверяем, свободна ли комната
            post.is_rented = True
            post.renter = request.user
            post.save()
            return redirect('web_room:home')  # Перенаправляем на главную при успешной аренде
        else:
            return render(request, 'web_room/post_detail.html', {
                'post': post,
                'error': 'Это объявление уже забронировано.'
            })

    return render(request, 'web_room/post_detail.html', {'post': post})

