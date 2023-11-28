from pydoc import stripid
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from forms import SignupForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect
from forms import SigninForm
from django.contrib.auth import logout
from .models import UserProfile
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


def homepage(request):
    # Add any necessary data or logic here
    return render(request, 'registration/homepage.html')


# def signup_view(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('success_view')
#     else:
#         form = SignupForm()
#     return render(request, 'registration/signup.html', {'form': form})

# @login_required
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Additional processing if needed
            return redirect('success_view')  # Redirect to the home page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'  # Create this template for the password reset form
    email_template_name = 'registration/password_reset_email.html'  # Create this template for the password reset email
    success_url = '/password_reset/done/'  # Redirect to this URL after a successful password reset


def signin_view(request):
    if request.method == 'POST':
        form = SigninForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage_view')
    else:
        form = SigninForm()
    return render(request, 'registration/signin.html', {'form': form})


def success_view(request):
    return render(request, 'registration/success.html')  # Replace 'success.html' with your success page template

def success_email_view(request):
    return render(request, 'registration/success_email.html')  # Replace 'success.html' with your success page template


def homepage_view(request):
    return render(request, 'registration/homepage.html')  # 'homepage.html' is the template for your homepage


def signout_view(request):
    # Log the user out
    logout(request)

    # Redirect to the homepage or any other page you prefer
    return render(request,
                  'registration/signed_out.html')  # redirect('signup')  # Replace 'homepage' with the name of your homepage URL pattern


# def signed_out(request):
#     return render(request, 'registration/signed_out.html')

def trading_view(request):
    # Your view logic here
    return render(request, 'registration/trading.html')


def livecurrencyrates_view(request):
    # Your view logic here
    return render(request, 'registration/livecurrencyrates.html')


def markettrends_view(request):
    # Your view logic here
    return render(request, 'registration/markettrends.html')


def payment_page(request):
    return render(request, 'payment/payment-page.html')
    # return redirect('payment_page')


def payment_confirm(request):
    if request.method == 'POST':
        user = get_object_or_404(UserProfile, user=request.user)
        user.save()
        messages.success(request, 'Payment has been completed successfully.')
        return render(request, 'registration/homepage.html')

    return render(request, 'payment/payment-page.html')


def successful_payment(request):
    return render(request, homepage)


def cancelled_payment(request):
    return render(request, homepage)


def place_order(request):
    return render(request, homepage)

from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
"""
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Send email
        send_mail(
            f'Contact Form - {subject}',
            f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}',
            'rahul.manjinder@yahoo.com',  # Replace with your email
            ['rahul.manjinder@gmail.com'],  # Replace with the recipient's email
            fail_silently=False,
        )

        # Redirect after successful form submission
        return HttpResponseRedirect('/success/')

    return render(request, 'registration/contact.html')

"""

# views.py

from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Send email to the team
        send_mail(
            f'Contact Form - {subject}',
            f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}',
            settings.DEFAULT_FROM_EMAIL,  # Use the default email address configured in your settings
            {email},
            #['recipient@example.com'],  # Replace with the recipient's email
            fail_silently=False,
        )

        # Send confirmation email to the user
        user_message = (
            f'Thank you for contacting us, {name}!\n\n'
            'Your feedback has been received and shared with the team.\n\n'
            'Best regards,\nThe Crptocurrency Backend Team'
        )
        send_mail(
            'Contact Form Submission Confirmation',
            user_message,
            settings.DEFAULT_FROM_EMAIL,  # Use the default email address configured in your settings
            [email],  # Send the confirmation email to the user
            fail_silently=False,
        )

        # Redirect after successful form submission
        return HttpResponseRedirect('success')

    return render(request, 'registration/contact.html')

"""
# crypto_rates/views.py
from django.shortcuts import render
import requests

def get_crypto_data():
    api_key = 'bea52cdee1bf044cf2c1d33fa6fd1a62'
    endpoint = f'http://api.coinlayer.com/list?access_key={api_key}'
    response = requests.get(endpoint)
    return response.json()

def crypto_dashboard(request):
    crypto_symbols = ['ETH', 'BTC', 'USDT', 'BNB', 'XRP', 'USDC', 'SOL', 'DOGE', 'TRX', 'LINK', 'AVAX', 'MATIC', 'DOT',
                      'DAI', 'LTC', 'SHIB', 'BCH', 'OKB', 'TUSD', 'XLM']

    crypto_data = get_crypto_data()
    
    # Assuming `crypto_data` is the JSON response from the CoinLayer API
    print(crypto_data)

    # Modify the following line based on the structure of the JSON response
    selected_crypto_data = {symbol: crypto_data[symbol] for symbol in crypto_symbols}

    #selected_crypto_data = {symbol: crypto_data['rates'][symbol] for symbol in crypto_symbols}

    context = {
        'crypto_data': selected_crypto_data,
    }

    return render(request, 'crypto-rates/crypto_dashboard.html', context)
"""

# views.py
from django.shortcuts import render
import requests

def crypto_dashboard(request):
    # CoinLayer API key
    api_key = "bea52cdee1bf044cf2c1d33fa6fd1a62"

    # Cryptocurrency symbols to display
    crypto_symbols = ['ETH', 'BTC', 'USDT', 'BNB', 'XRP', 'USDC', 'SOL', 'DOGE', 'TRX', 'LINK', 'AVAX', 'MATIC', 'DOT', 'DAI', 'LTC', 'SHIB', 'BCH', 'OKB', 'TUSD', 'XLM']

    # Get live cryptocurrency rates from CoinLayer API
    response = requests.get(f'http://api.coinlayer.com/list?access_key={api_key}')
    crypto_data = response.json()

    # Get data for selected cryptocurrencies
    selected_crypto_data = crypto_data.get('crypto', {})

    # Prepare a list of dictionaries for rendering in the template
    crypto_list = []
    for symbol, data in selected_crypto_data.items():
        print("Symbol:- ",symbol)
        print("Data:- ", data)
        #'cryptocurrency_logo': data.get('icon_url', ''),
        
        crypto_dict = {
            'serial_number': len(crypto_list) + 1,
            'cryptocurrency_name': data.get('name', ''),
            'cryptocurrency_logo': data.get('icon_url', ''),
            # 'rate': data.get('rate', ''),
            'max_supply': data.get('max_supply', ''),  # Add max_supply to the dictionary
            'name_full': data.get('name_full', ''),    # Add name_full to the dictionary
            'symbol': data.get('symbol', ''),          # Add symbol to the dictionary
        }
        crypto_list.append(crypto_dict)

    # Render the template with the list of dictionaries
    return render(request, 'crypto-rates/crypto_dashboard.html', {'crypto_list': crypto_list})

def about_us(request):
    return render(request, 'static-pages/about_us.html')
