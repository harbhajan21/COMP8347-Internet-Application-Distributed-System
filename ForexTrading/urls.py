"""
URL configuration for ForexTrading project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

urlpatterns = [
    path("admin/", admin.site.urls),
]
from django.urls import path
from myApp import views

urlpatterns = [
    # ... Other URL patterns ...
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('success/', views.success_view, name='success_view'),
    path('homepage/', views.homepage_view, name='homepage_view'),
    path('signout/', views.signout_view, name='signout'),
    path('trading/', views.trading_view, name='trading'),
    path('livecurrencyrates/', views.livecurrencyrates_view, name='livecurrencyrates'),
    path('markettrends/', views.markettrends_view, name='markettrends'),

]