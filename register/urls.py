from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('login', auth_views.LoginView.as_view(template_name='Login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='Logout.html'), name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('create', views.createuser, name='createuser'),
    path('follow', views.follow, name='followpage'),
    path('comment', views.comment, name='commentPage'),
    path('post', views.post, name='postPage'),
    path('like', views.like, name='likepage'),
    path('watch', views.dashboard, name='watchPage'),

]
