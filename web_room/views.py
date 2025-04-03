from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from users.models import ViewHistory
from .forms import AnnouncementForm, SearchRoomForm
from .models import Announcement, RentalHistory
from django.utils.timezone import now


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

    # Аннотируем средний рейтинг
    posts = posts.annotate(avg_rating=Avg('reviews__rating'))

    # Обработка сортировки
    sort = request.GET.get("sort", "date_desc")
    sort_mapping = {
        "rating_asc": "avg_rating",
        "rating_desc": "-avg_rating",
        "date_asc": "created_at",
        "date_desc": "-created_at",
        "price_asc": "price",
        "price_desc": "-price",
    }
    posts = posts.order_by(sort_mapping.get(sort, "-created_at"))

    # Пагинация
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

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

    # Записываем факт просмотра объявления
    if request.user.is_authenticated:
        ViewHistory.objects.get_or_create(user=request.user, post=post, defaults={"viewed_at": now()})

    if request.method == 'POST':
        if not post.is_rented:
            post.is_rented = True
            post.renter = request.user
            post.rented_at = now()
            post.save()

            # Записываем аренду в историю
            RentalHistory.objects.create(user=request.user, announcement=post, rented_at=now())

            return redirect('web_room:home')

        elif post.is_rented and post.renter == request.user:
            # Отмена аренды
            post.is_rented = False
            post.renter = None
            post.rented_at = None
            post.save()

            # Записываем дату отмены аренды
            history_entry = RentalHistory.objects.filter(user=request.user, announcement=post).last()
            if history_entry and history_entry.canceled_at is None:
                history_entry.canceled_at = now()
                history_entry.save()

            return redirect('web_room:home')

    return render(request, 'web_room/post_detail.html', {'post': post})

@login_required
def view_history(request):
    history = ViewHistory.objects.filter(user=request.user).select_related('post')[:100]
    return render(request, 'users/ad_history.html', {'history': history})


@login_required
def rental_history(request):
    history = RentalHistory.objects.filter(user=request.user).order_by('-rented_at')

    return render(request, 'users/rental_history.html', {'history': history})