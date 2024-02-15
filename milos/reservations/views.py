from django.shortcuts import render, get_object_or_404, redirect
#from django.http import HttpResponse
from .models import Post
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView
from django.core.paginator import Paginator
from .forms import ResUpdateForm, ReservationForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# def home(request):
#     return HttpResponse('<h1>Blog Home</h1>')

posts = Post.objects.all()


def home(request):
    post_list = Post.objects.all().order_by('-datum')
    perpage = request.GET.get('perpage', 10)
    try:
        perpage = int(perpage)
        if perpage < 1:  
            perpage = 10
    except ValueError:
        perpage = 10  
    paginator = Paginator(post_list, perpage)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'perpage': perpage  
    }
    return render(request, 'reservations/home.html', context)


def reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  
    else:
        form = ReservationForm()

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
        if self.request.user == post.ime:
            return True
        return False

class DeleteResView(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'reservations/reservation_delete.html'
    success_url = reverse_lazy('reservation-home')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.ime:
            return True
        return False