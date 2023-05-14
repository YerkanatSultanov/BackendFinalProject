from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='home_page'),
    path('register/', views.register, name='register'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.my_logout_view, name='logout'),
    path('book_search',  views.search_books, name='search_book'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/', views.profile_page, name='profile'),
    path('category/<int:cat_id>/', views.show_category, name='category'),
    path('cart/', views.cart, name='cart'),
    path('book_detail/<int:book_pk>', views.book_detail, name="book_detail"),
    path('category/<int:book_pk>', views.add_to_cart, name='add_to_cart')
]
