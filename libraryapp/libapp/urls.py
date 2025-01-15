from django.contrib import admin
from django.urls import path
from libapp import views

urlpatterns = [
    path('api/login/', views.login, name='login'),
    path('api/signup/', views.signup, name='signup'),
    path('api/users/UsersList/', views.UsersList, name='UsersList'),
    path('api/users/deleteUser/', views.deleteUser, name='deleteuser'),
    path('api/books/returnbook/',views.returnbook,name='returnbook'),
    path('api/books/search/', views.search, name='search'),
    path('api/books/borrow/',views.borrow,name='borrow'),
    #path('api/test/', views.test, name='test')
]
