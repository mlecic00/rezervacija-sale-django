from django.shortcuts import render, get_object_or_404, redirect
#from django.http import HttpResponse
#from django.forms.models import model_to_dict #ovo kaze da lakse mozemo da prikazemo polja u modelu koja hocemo  
#from rest_framework.response import Response 
from rest_framework.decorators import api_view
from .models import Post
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView
from django.core.paginator import Paginator
from .forms import ResUpdateForm, ReservationForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date, datetime
from django.db.models import Q
# def home(request):
#     return HttpResponse('<h1>Blog Home</h1>')

posts = Post.objects.all()

@api_view(["GET", "POST"])
def home(request):
    # posts = Post.objects.all()
    posts = Post.objects.all().order_by('-datum')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search_query = request.GET.get('search_query', '')

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            posts = posts.filter(datum__range=(start_date, end_date))
        except ValueError:
            pass

    if search_query:
        posts = posts.filter(
            Q(sala__icontains=search_query) |
            Q(ime__icontains=search_query) |
            Q(razlog__icontains=search_query)
        )
    # odavde ide paginacija
    perpage = request.GET.get('perpage', 10)
    try:
        perpage = int(perpage)
        if perpage < 1:  
            perpage = 10
    except ValueError:
        perpage = 10  
    paginator = Paginator(posts, perpage)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'start_date': start_date,
        'end_date': end_date,
        'search_query': search_query,
        'perpage': perpage,
        'page_obj': posts,
        'paginator': paginator,
        'today': date.today()
    }
    return render(request, 'reservations/home.html', context)


def reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST, request = request)
        if form.is_valid():
            form.save()
            return redirect('/')  
    else:
        form = ReservationForm(request = request)

    return render(request, 'reservations/reservation.html', {'form': form})

def reservationDetails(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'reservations/reservation_details.html', {'post': post})


class UpdateResView(UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'reservations/reservation_update.html'
    form_class = ResUpdateForm

    def test_func(self):
        post = self.get_object()
        if self.request.user.is_superuser:
            return True
        if self.request.user == post.ime:
            return True
        return False

class DeleteResView(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'reservations/reservation_delete.html'
    success_url = reverse_lazy('reservation-home')

    def test_func(self):
        post = self.get_object()
        if self.request.user.is_superuser:
            return True
        if self.request.user == post.ime:
            return True
        return False