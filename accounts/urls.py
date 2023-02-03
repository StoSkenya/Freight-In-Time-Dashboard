from django.urls import path

from .views import (home,signup,create_profile,user_login,logout_view,get_sum_quotes)

urlpatterns = [
    path('',home,name='home'),
    path("login", user_login, name="login"),
    path('signup',signup,name='signup'),
    path('create_profile',create_profile,name='create_profile'),
    path("logout",logout_view,name="logout"),
    path('sumquotes', get_sum_quotes,name='sumquotes'),  
]