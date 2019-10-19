from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('mine/',views.mine, name="mine"),
    path('', views.index, name="index"),
]