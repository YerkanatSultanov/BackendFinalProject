from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import *
from .forms import RegistrationForm


def index(request):
    posts = Book.objects.all()
    categories = Category.objects.all()
    context = {
        'posts': posts,
        'categories': categories
    }
    return render(request, 'reviews/main.html', context=context)




def register(request):
    form = RegistrationForm()

    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            messages.error(request, 'Password don\'t match')
        elif User.objects.filter(username=uname).exists():
            messages.error(request, 'User already exists')
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')

    context = {'f': form}

    return render(request, 'reviews/registration.html', context)


def log_in(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home_page")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()

    context = {'f': form}
    return render(request, 'reviews/login.html', context)


def log_out(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return render(request, "base.html")
