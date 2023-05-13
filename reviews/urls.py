from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home_page'),
    path('register/', views.register, name='register'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.my_logout_view, name='logout'),
    path('book_search',  views.search_books, name='search_book'),
    path('profile/', views.profile, name='profile'),
    path('category/<int:cat_id>/', views.show_category, name='category')
]
