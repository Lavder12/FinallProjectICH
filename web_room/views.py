from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AnnouncementForm, SearchRoomForm
from .models import Announcement


# Create your views here.
def index(request):
    return render(request, 'main_page.html')


def find_room(request):
    form = SearchRoomForm(request.GET)
    posts = Announcement.objects.all()

    # Обрабатываем фильтры
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

    # Обрабатываем сортировку
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

    return render(request, "find_room.html", {
        "form": form,
        "page_obj": page_obj,
        "sort": sort,
    })



@login_required
def register_room(request):
    if request.method == "POST":
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcment = form.save(commit=False)
            announcment.author = request.user
            announcment.save()
            return redirect('home')
    else:
        form = AnnouncementForm()
    return render(request, "register_room.html", {"form": form})


def post_detail(request, pk):
    post = get_object_or_404(Announcement, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

# def show_post(request):
#     form = AnnouncementForm()
#     return render(request, 'women/register_room.html')
