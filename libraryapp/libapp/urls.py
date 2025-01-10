from django.contrib import admin
from django.urls import path
from libapp import views

urlpatterns = [
    path('api/login/', views.login, name='login'),
    path('api/signup/', views.signup, name='signup'),
    path('api/borrow/',views.borrow,name='borrow'),
    path('api/returnbook/',views.returnbook,name='returnbook'),
    path('api/search/', views.search, name='search'),
]
