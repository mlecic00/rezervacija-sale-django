from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


class UserRegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,("Ulogovani ste!"))
            return redirect('reservation-home')  
        else:
            return render(request, 'users/login.html', {'error_message': 'Pokusajte ponovo...'})
    else:
        return render(request, 'users/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, ("Uspesno ste izlogovani!"))
    return redirect('reservation-home')