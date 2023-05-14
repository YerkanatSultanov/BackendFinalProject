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
        'posts': posts,
        'categories': categories,
        'cat_selected': 0
    }
    return render(request, 'reviews/main.html', context=context)


# def filter_books(request):
#     return render(request, 'reviews/main.html')

def search_books(request):
    search_text = request.GET.get("search", "")
    form = SearchForm(request.GET)
    books = set()

    if form.is_valid() and form.cleaned_data["search"]:
        search = form.cleaned_data["search"]
        search_in = form.cleaned_data.get("search_in") or "title"

        if search_in == "title":
            books = Book.objects.filter(title__icontains=search)
        else:
            Contributor.objects.filter(first_names__icontains=search)


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
def add_to_cart(request, book_id):
    book = Book.objects.get(id=book_id)
    cart_, created = Cart.objects.get_or_create(user=request.user, book=book)
    if not created:
        cart_.quantity += 1
        cart_.save()
        messages.success(request, 'Product quantity updated.')
    else:
        messages.success(request, 'Product added to cart.')
    return redirect('cart')


@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    context = {
        'cart_items': cart_items
    }
    return render(request, 'reviews/cart.html', context)


@login_required
def remove_from_cart(request, book_id):
    cart_item = Cart.objects.get(user=request.user, book_id=book_id)
    if cart_item:
        cart_item.delete()
        messages.success(request, "Item removed from cart")
    else:
        messages.warning(request, "Item not in cart")

    return redirect('cart')
