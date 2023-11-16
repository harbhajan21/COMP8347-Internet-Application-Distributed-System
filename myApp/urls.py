from django.urls import path, include
from myApp import views

urlpatterns = [
    # ... Other URL patterns ...
    path('', views.homepage, name='homepage'),  # Set homepage.html as the default homepage
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('success/', views.success_view, name='success_view'),
    path('homepage/', views.homepage_view, name='homepage_view'),
    # path('signed_out/', views.signed_out, name='signed_out'),
    path('signout/', views.signout_view, name='signout'),
    path('trading/', views.trading_view, name='trading'),
    path('livecurrencyrates/', views.livecurrencyrates_view, name='livecurrencyrates'),
    path('markettrends/', views.markettrends_view, name='markettrends'),
    path('payment/', views.payment_page, name='payment_page'),
    path('payment-confirm/', views.payment_confirm, name='payment_confirm'),
    path('place_order/',views.place_order, name='place_order')
    # path('paypal/', include('paypal.standard.ipn.urls')),



]

