from django.contrib import admin
from django.urls import path
from libapp.views import home,login

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
]
