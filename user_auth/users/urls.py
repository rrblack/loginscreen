from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView
from django.urls import path, include
from . import views



urlpatterns = [
    path('', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('top_page/', views.top_page, name='top_page'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('mail_check/' , views.mail_check, name='mail_check'),

    ]
