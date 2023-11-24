from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path("simple_function", views.simple_func)
]