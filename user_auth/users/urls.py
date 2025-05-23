from django.contrib.auth.views import LoginView
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.root_redirect),
    path('login/', views.users_login, name='user_login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('top_page/', views.login_success, name='top_page'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('mail_check/' , views.mail_check, name='mail_check'),
    path('mail_verification/', views.mail_verification, name='mail_verification'),
    ]
