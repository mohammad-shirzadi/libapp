from django.contrib import admin
from django.urls import path
from libapp import views

urlpatterns = [
    path('',views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('boroow/<str:borrow>',views.borrow,name='borrow')
]
