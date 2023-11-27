import json
from datetime import datetime
from pydoc import stripid

from alpha_vantage.timeseries import TimeSeries
from django.contrib.auth import login
import requests
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from forms import SignupForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect
from forms import SigninForm
from django.contrib.auth import logout
from .models import UserProfile, Payment
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
    # Your API key from Alpha Vantage
    # api_key = 'F8FLNKTMJ6DRQNE6'
    # interval = '60min'  # Set the desired interval
    #
    # url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval={interval}&apikey={api_key}'
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
        'error': 'Time series data not found'
    }
    return render(request, 'registration/trading.html', context)


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
    success = False
    if request.method == 'POST':
        amount = request.POST.get('amount')
        card_number = request.POST.get('card_number')
        user_name = request.POST.get('user_name')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        payment_option = request.POST.get('payment_option')

        if len(amount) > 10 or not amount.isdigit():
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

        # Create and save the payment transaction
        payment = Payment(
            amount=amount,
            card_number=card_number,
            user_name=user_name,
            expiry_date=expiry_date,
            cvv=cvv,
            payment_option=payment_option
        )
        payment.save()

        # Redirect or show a success message
        success = True   # Replace 'success_url' with your URL name

    return render(request, 'payment/payment-page.html', {'success': success})


def successful_payment(request):
    return render(request, homepage)


def cancelled_payment(request):
    return render(request, homepage)


def place_order(request):
    return render(request, homepage)


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
