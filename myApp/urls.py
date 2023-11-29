from django.urls import path, include
from myApp import views
# from django.urls import path
# from .views import contact
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # ... Other URL patterns ...
    path('', views.homepage, name='homepage'),  # Set homepage.html as the default homepage
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('success/', views.success_view, name='success_view'),
    path('success_email/', views.success_email_view, name='success_email_view'),
    path('homepage/', views.homepage_view, name='homepage_view'),
    # path('signed_out/', views.signed_out, name='signed_out'),
    path('signout/', views.signout_view, name='signout'),
    path('trading/', views.trading_view, name='trading'),
    #path('livecurrencyrates/', views.livecurrencyrates_view, name='livecurrencyrates'),
    path('markettrends/', views.markettrends_view, name='markettrends'),
    path('payment/', views.payment_page, name='payment_page'),
    path('payment-confirm/', views.payment_confirm, name='payment_confirm'),
    path('place_order/',views.place_order, name='place_order'),
    # path('paypal/', include('paypal.standard.ipn.urls')),
    path('contact/', views.contact, name='contact'),
    path('contact_success', views.contact_success, name='contact_success'),

    path('livecurrencyrates/', views.crypto_dashboard, name='crypto_dashboard'),
    path('visualize/', views.visualize_dashboard, name='visualize_dashboard'),
    #path('crypto-to-crypto/', views.crypto_to_crypto, name='crypto-to-crypto'), 
    #path('crypto-to-currency/', views.crypto_to_currency, name='crypto-to-currency'),
    path('crypto_prices/', views.crypto_prices, name='crypto_prices'),
    path('about-us/', views.about_us, name='about_us'),
     path('careers/', views.careers, name='careers'),
path('get_crypto_data/', views.get_crypto_data, name='get_crypto_data'),

  
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)