import json
from decimal import Decimal
from datetime import datetime
from pydoc import stripid

from _decimal import InvalidOperation
from alpha_vantage.timeseries import TimeSeries
from django.contrib.auth import login
import requests
from django.core.exceptions import ValidationError
from django.db.models import Max
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from forms import SignupForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect
from forms import SigninForm
from django.contrib.auth import logout
from .models import UserProfile, Payment, Transaction
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


def homepage(request):
    api_key = 'coinrankingae631d1d5459748c6ec3a765f23471d6c612b840fc2d9938'
    headers = {'x-access-token': api_key}
    api_url = "https://api.coinranking.com/v2/coins"

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json().get("data", {}).get("coins", [])[:100]

        # Assuming you have payment history data, replace the following line with your actual data retrieval logic
        payment_history = Payment.objects.filter(user=request.user).order_by('-transaction_date')

        return render(request, 'registration/homepage.html', {
            'coins': data,
        })
    # return render(request, 'registration/homepage.html')


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
                return redirect('homepage')
    else:
        form = SigninForm()
    return render(request, 'registration/signin.html', {'form': form})


def success_view(request):
    return render(request, 'registration/success.html')  # Replace 'success.html' with your success page template


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
    symbol = request.GET.get('symbol', 'DefaultSymbol')
    name = request.GET.get('name', 'DefaultName')
    price = request.GET.get('price', '0')

    # Your API key from Alpha Vantage
    # api_key = 'F8FLNKTMJ6DRQNE6'
    # interval = '60min'  # Set the desired interval
    #
    # url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval={interval}&apikey={api_key}'
    #url = f'https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol=ETH&market=USD&interval={interval}&outputsize=full&apikey={api_key}'
    # response = requests.get(url)
    # data = response.json()
    # print("Api response:", data)
    #
    # # The key typically includes the interval, e.g., "Time Series Crypto (5min)"
    # # Check the exact structure of your response and replace the key accordingly
    # time_series_key = f"Time Series ({interval})"
    # print(time_series_key)
    #
    # if time_series_key in data:
    #     time_series_data = data[time_series_key]
    #
    #     # Extract the closing prices and timestamps
    #     chart_data = [float(value['4. close']) for (key, value) in time_series_data.items()]
    #     chart_labels = [key for (key, value) in time_series_data.items()]
    #
    #     context = {
    #         'data': json.dumps(chart_data),
    #         'labels': json.dumps(chart_labels),
    #     }
    # else:
    #     # Handle the error or set default values
    #     context = {
    #         'data': json.dumps([]),
    #         'labels': json.dumps([]),
    #         'error': 'Time series data not found in the API response',
    #     }

    context = {
        'data': json.dumps([]),
        'labels': json.dumps([]),
        'error': 'Time series data not found',
        'coin_symbol': symbol,
        'coin_name': name,
        'coin_price': price,
    }
    return render(request, 'registration/trading.html', context)


def livecurrencyrates_view(request):
    # Your view logic here
    return render(request, 'registration/livecurrencyrates.html')


def markettrends_view(request):
    # Your view logic here
    return render(request, 'registration/markettrends.html')


@login_required
def account_details(request):
    return render(request, 'registration/account_details.html', {'request': request})


def payment_page(request):
    return render(request, 'payment/payment-page.html')
    # return redirect('payment_page')


@login_required
def payment_confirm(request):
    success = False
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount'))
        except InvalidOperation:
            raise ValidationError("Invalid Amount Format")
        card_number = request.POST.get('card_number')
        user_name = request.POST.get('user_name')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        payment_option = request.POST.get('payment_option')

        if amount <= 0.00 or amount > 10000.00:
            raise ValidationError("Invalid Amount Value")
        # Validate card number, CVV, and other fields if necessary
        if len(card_number) != 16 or not card_number.isdigit():
            raise ValidationError("Invalid card number")
        if len(cvv) not in [3, 4] or not cvv.isdigit():
            raise ValidationError("Invalid CVV")

        # Convert expiry date to a date object
        try:
            expiry_date = datetime.strptime(expiry_date, '%m/%y').date()
        except ValueError:
            raise ValidationError("Invalid expiry date format, use MM/YY")

        latest_payment = Payment.objects.filter(user=request.user).aggregate(Max('account_balance'))
        latest_balance = latest_payment['account_balance__max'] or Decimal(0)

        print("decimal", latest_balance, "amount", amount)
        new_balance = latest_balance + amount

        # Create and save the payment transaction
        payment = Payment(
            user=request.user,  # Associate with the logged-in user
            amount=amount,
            card_number=card_number,
            user_name=user_name,
            expiry_date=expiry_date,
            cvv=cvv,
            payment_option=payment_option,
            transaction_date=timezone.now(),
            account_balance=new_balance
        )
        payment.save()

        success = True

    if success:
        # Add a message and redirect to the homepage
        return render(request, 'payment/payment-page.html', {'success': success, 'redirect_url': 'homepage.html'})
    else:
        return render(request, 'payment/payment-page.html', {'success': success})


def successful_payment(request):
    return render(request, homepage)


def cancelled_payment(request):
    return render(request, homepage)


def place_order(request):
    return render(request, homepage)


## Functions for Highligths Start
from django.shortcuts import render
import requests


def dashboard(request):
    api_key = 'coinrankingae631d1d5459748c6ec3a765f23471d6c612b840fc2d9938'
    headers = {'x-access-token': api_key}
    # response = requests.get("https://api.coinranking.com/v2/coins", headers=headers)
    # data = response.json().get('data', {}).get('coins', [])[:50]  # Get the top 50 coins
    api_url = "https://api.coinranking.com/v2/coins"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json().get("data", {}).get("coins", [])[:100]
        formatted_currencies = []

        # Create Currency objects with data from the CoinCap API
        for coin in data:
            coin_id = coin.get('uuid', '')
            name = coin.get('name', '')
            symbol = coin.get('symbol', 'BTS')
            icon_url = coin.get('iconUrl', 'https://cdn.coinranking.com/bOabBYkcX/bitcoin_btc.svg')

    return render(request, 'highlights/dashboard.html', {'coins': data})


def buy_coin(request, symbol):
    # Logic for buying the coin
    return render(request, 'highlights/buy_coin.html', {'symbol': symbol})


def sell_coin(request, symbol):
    # Logic for selling the coin
    return render(request, 'highlights/sell_coin.html', {'symbol': symbol})


def dashboard(request):
    api_key = 'coinrankingae631d1d5459748c6ec3a765f23471d6c612b840fc2d9938'
    headers = {'x-access-token': api_key}
    api_url = "https://api.coinranking.com/v2/coins"

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json().get("data", {}).get("coins", [])[:100]

        # Extracting top 5 and bottom 5 coins
        top_5_coins = data[:5]
        bottom_5_coins = data[-5:]

        # Assuming you have payment history data, replace the following line with your actual data retrieval logic
        payment_history = Payment.objects.filter(user=request.user).order_by('-transaction_date')

        return render(request, 'highlights/highlights.html', {
            'top_5_coins': top_5_coins,
            'bottom_5_coins': bottom_5_coins,
            'payment_history': payment_history,
            'coins': data,
        })


## Functions for Highligths Ends
def my_view(request):
    # Get your data here, possibly from a database or an external service
    data = [62000, 62500, 61500, 63000]  # Example data points
    labels = ["3 PM", "6 PM", "9 PM", "12 AM"]  # Example labels

    # Serialize your data and labels to JSON
    data_json = json.dumps(data)
    labels_json = json.dumps(labels)

    return render(request, 'registration/trading.html', {
        'data': data_json,
        'labels': labels_json
    })


@login_required
def place_order(request):
    if request.method == 'POST':
        # Extract data from the form
        coin_symbol = request.POST.get('coin_symbol')
        coin_name = request.POST.get('coin_name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        transaction_type = request.POST.get('transaction_type')  # 'BUY' or 'SELL'

        # Assuming 'request.user' is the current user
        max_balance_payment = Payment.objects.filter(user=request.user).aggregate(Max('account_balance'))
        payment = Payment.objects.get(user=request.user, account_balance=max_balance_payment['account_balance__max'])
        # payment = Payment.objects.get(user=request.user)

        try:
            transaction = Transaction(
                payment=payment,
                coin_symbol=coin_symbol,
                coin_name=coin_name,
                price_per_coin=price,
                quantity=quantity,
                transaction_type=transaction_type
            )
            transaction.save()
            messages.success(request, 'Transaction successful.')
        except ValidationError as e:
            messages.error(request, str(e))

    return redirect('homepage')
