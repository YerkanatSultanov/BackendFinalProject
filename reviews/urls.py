from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home_page'),
    path('register/', views.register, name='register'),
    path('login/', views.log_in, name='login')
]
