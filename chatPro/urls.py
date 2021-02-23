from django.contrib import admin
from django.urls import path
from chatApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.chat, name='app-chat'),
    path('chat/', views.chat, name='app-chat'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('create-user/', views.create_user, name='create-user'),
   
]
