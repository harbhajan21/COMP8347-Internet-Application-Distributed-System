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

