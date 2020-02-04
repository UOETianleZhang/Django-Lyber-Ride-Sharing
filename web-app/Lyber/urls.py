"""Lyber URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# Use include() to add URLS from the catalog application and authentication system
from django.urls import include
from orders.views import signup_view, user_page_view, home_view, create_driver_view
from orders.driver_view import driver_page_view

# urlpatterns = [
#     path('orders/', include('orders.urls')),
#     path('admin/', admin.site.urls),
#     path('accounts/', include('django.contrib.auth.urls')),
#     path('signup/', signup_view),
# ]

urlpatterns = [
    path('', home_view, name='home'),
    path('orders/', include('orders.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup_view, name='signUp'),
    path('userPage/', user_page_view, name='userPage'),
    path('driverPage/', driver_page_view , name='driverPage'),
    path('driver/newDriver', create_driver_view , name='createDriverPage')
]