from django.contrib import admin
from django.urls import path
from . import views
from .views import delete_user, registerview, LoginView, UserView , LogoutView, updateuser

urlpatterns = [
    path('index', views.index , name="index"),
    path('', views.index , name="index"),
    path('register',registerview.as_view()),
    path('Login', LoginView.as_view()),
    path('userv', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('update',updateuser.as_view()),
    path('del',delete_user, name="delete_user"),

]
