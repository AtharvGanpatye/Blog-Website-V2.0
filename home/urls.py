from django.contrib import admin
from django.urls import path, include
from home import views
from blog.views import register
from django.contrib.auth import views as auth_views

app_name = 'home'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('register/', register, name='register'),
    
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='home/home.html'), name='logout'),

]
