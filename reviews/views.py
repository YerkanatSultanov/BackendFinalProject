from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from .models import *


def index(request):
    posts = Book.objects.all()
    categories = Category.objects.all()
    context = {
        'title': "Каталог",
        'posts': posts,
        'categories': categories,
        'cat_selected': 0
    }
    return render(request, 'reviews/main.html', context=context)


# def filter_books(request):
#     return render(request, 'reviews/main.html')

def search_books(request):
    search_term = request.GET.get('search_term')
    results = []
    categories = Category.objects.all()
    if search_term:
        results = Book.objects.filter(title__icontains=search_term) | Book.objects.filter(publisher__name__icontains=search_term)
    context = {
        'title': "Результат поиска",
        'posts': results,
        'categories': categories
    }
    return render(request, "reviews/main.html", context=context)


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
                return redirect("home_page")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()

    context = {'f': form}
    return render(request, 'reviews/login.html', context)


def my_logout_view(request):
    logout(request)
    return redirect('home_page')


@login_required
def profile_page(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    return render(request, 'reviews/profile.html', {
        'user': request.user,
        'profile': profile
    })


@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
        user = request.user

    return render(request, 'reviews/edit_profile.html', {
        'form': form,
        'profile': profile,
        'user': user
    })


def show_category(request, cat_id):
    posts = Book.objects.filter(category=cat_id)
    cats = Category.objects.all()
    context = {
        'posts': posts,
        'categories': cats,
        'cat_selected': cat_id
    }

    return render(request, 'reviews/category_all_books.html', context=context)


def book_detail(request, book_pk, review_pk=None):
    book = get_object_or_404(Book, pk=book_pk)
    reviews = book.review_set.all()

    if review_pk is not None:
        review = get_object_or_404(Review, book_id=book_pk, pk=review_pk)
    else:
        review = None

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            updated_review = form.save(False)
            updated_review.book = book

            if review is None:
                updated_review.creator = request.user.username
                messages.success(request, "Review for \"{}\" created.".format(book))

            updated_review.save()
            return redirect("book_detail", book.pk)
    else:
        form = ReviewForm(instance=review)

    context = {
        'book': book,
        'reviews': reviews,
        "form": form,
        "instance": review,
        "model_type": "Review",
        "related_instance": book,
        "related_model_type": "Book"
    }
    return render(request, 'reviews/reviews_book.html', context=context)


@login_required
def view_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()
    cost = 0
    for i in cart_items:
        cost += int (i.book.price)
    return render(request, 'reviews/cart.html', {'cart_items': cart_items, 'cost': cost})


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


@login_required
def remove_from_cart(request, book_id):
    cart_item = CartItem.objects.get(cart__user=request.user, book_id=book_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')
