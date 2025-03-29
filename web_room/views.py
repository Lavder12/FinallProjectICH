from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AnnouncementForm
from .models import Announcement

# Create your views here.
def index(request):
    return render(request, 'main_page.html')


def find_room(request):
    posts = Announcement.objects.all().order_by('-created_at')  # Получаем все посты
    paginator = Paginator(posts,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'find_room.html', {'page_obj': page_obj})

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