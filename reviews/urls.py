from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home_page'),
    path('register/', views.register, name='register'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.my_logout_view, name='logout'),
    path('book_search', views.search_books, name='search_book'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/', views.profile_page, name='profile'),
    path('category/<int:cat_id>/', views.show_category, name='category'),
    path('cart/', views.view_cart, name='cart'),
    path('book_detail/<int:book_id>', views.book_detail, name="book_detail"),
    path('add_to_cart/<int:book_id>', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:book_id>/', views.remove_from_cart, name='remove_item')
]
