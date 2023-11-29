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
from django.urls import reverse
from django.conf import settings

# views.py
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse

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
            {email},  # Replace with the recipient's email
            fail_silently=False,
        )

        # Redirect after successful form submission
        return render(request, 'registration/contact_success.html', {'message': 'success'})

    return render(request, 'registration/contact.html')


# views.py
from django.shortcuts import render
def contact_success(request, message):
    context = {'message': 'Sent Sucessfully'}
    return render(request, 'registration/contact_success.html', context)

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

    # Get live rates from another API
    response_rates = requests.get('http://api.coinlayer.com/live?access_key=bea52cdee1bf044cf2c1d33fa6fd1a62')
    rates_data = response_rates.json()

    # Get data for selected cryptocurrencies
    selected_crypto_data = crypto_data.get('crypto', {})

    # Prepare a list of dictionaries for rendering in the template
    crypto_list = []
    i=0
    for symbol, data in selected_crypto_data.items():
        rate = rates_data['rates'].get(symbol, '')  # Get the rate from the rates_data
        #print("RATE:- ", rate)
        #print("Symbol:- ",symbol)
        #print("Data:- ", data)
        #if i==0:
        #    print("selected_crypto_data.items:- ",selected_crypto_data)
        #    i=i+1
        #'cryptocurrency_logo': data.get('icon_url', ''),
        
        crypto_dict = {
            'serial_number': len(crypto_list) + 1,
            'cryptocurrency_name': data.get('name', ''),
            'cryptocurrency_logo': data.get('icon_url', ''),
            'rate': rate,
            'max_supply': data.get('max_supply', ''),  # Add max_supply to the dictionary
            'name_full': data.get('name_full', ''),    # Add name_full to the dictionary
            'symbol': data.get('symbol', ''),          # Add symbol to the dictionary
        }
        crypto_list.append(crypto_dict)

    # Render the template with the list of dictionaries
    return render(request, 'crypto-rates/crypto_dashboard.html', {'crypto_list': crypto_list})

def about_us(request):
    return render(request, 'static-pages/about_us.html')


    # views.py
# views.py


from django.shortcuts import render
import requests
import plotly.express as px

def convert_to_million_usd(value):
    return f"${value / 1_000_000:.2f} Million USD"

def convert_to_million_billion_trillion(value):
    magnitude_labels = [(1_000_000_000_000, 'Trillion'), (1_000_000_000, 'Billion'), (1_000_000, 'Million')]

    for magnitude, label in magnitude_labels:
        if value >= magnitude:
            return f"${value / magnitude:.2f} {label} "

    return f"${value:.2f} "

def visualize_dashboard(request):
    # CoinLayer API key
    api_key = "bea52cdee1bf044cf2c1d33fa6fd1a62"

    # Get live cryptocurrency rates from CoinLayer API
    response = requests.get(f'http://api.coinlayer.com/list?access_key={api_key}')
    crypto_data = response.json()

    # Get live rates from another API
    response_rates = requests.get('http://api.coinlayer.com/live?access_key=bea52cdee1bf044cf2c1d33fa6fd1a62')
    rates_data = response_rates.json()

    # Get data for selected cryptocurrencies
    selected_crypto_data = crypto_data.get('crypto', {})

    # Prepare a list of dictionaries for rendering in the template
    crypto_list = []
    for symbol, data in selected_crypto_data.items():
        rate = rates_data['rates'].get(symbol, 0)  # Get the rate from the rates_data
        max_supply_str = data.get('max_supply', 'N/A')
        
        # Convert max_supply to integer, handling 'N/A' cases
        try:
            max_supply = int(max_supply_str)
        except ValueError:
            max_supply = 0

        crypto_dict = {
            'symbol': data.get('symbol', ''),
            'name_full': data.get('name_full', ''),
            'max_supply': max_supply,
            'rate': rate,
        }
        crypto_list.append(crypto_dict)

    # Sort crypto_list by rate and max_supply
    crypto_list.sort(key=lambda x: x['rate'], reverse=True)
    top_10_expensive = crypto_list[:10]
    print("Top 10 Expensive", top_10_expensive)
    crypto_list.sort(key=lambda x: x['max_supply'], reverse=True)
    top_10_max_supply = crypto_list[:10]
    print("Top 10 MAX SUPPLY", top_10_max_supply)

    # Bar plot for top 10 expensive cryptocurrencies
    fig_expensive = px.bar(top_10_expensive, x='name_full', y='rate', title='Top 10 Expensive Cryptocurrencies')
    fig_expensive.update_layout(xaxis_title='Cryptocurrency', yaxis_title='Rate (USD)',hovermode='x unified')


    # Bar plot for top 10 cryptocurrencies by max supply
    fig_max_supply = px.bar(top_10_max_supply, x='name_full', y='max_supply', title='Top 10 Cryptocurrencies by Max Supply')
    fig_max_supply.update_layout(xaxis_title='Cryptocurrency', yaxis_title='Max Supply',hovermode='x unified')

    # Calculate KPIs
    average_rate = sum(crypto['rate'] for crypto in top_10_expensive) / len(top_10_expensive)
    average_max_supply = sum(crypto['max_supply'] for crypto in top_10_max_supply) / len(top_10_max_supply)

    return render(
        request,
        'crypto-rates/visualize_dashboard.html',
        {'fig_expensive': fig_expensive.to_html(), 
         'fig_max_supply': fig_max_supply.to_html(),
         'top_10_expensive': top_10_expensive, 
         'top_10_max_supply': top_10_max_supply,
        'average_rate': convert_to_million_usd(average_rate),
       'average_max_supply': convert_to_million_billion_trillion(average_max_supply),
  }
    )


# crypto_converter/views.py

import requests
from django.shortcuts import render

API_KEY = 'bea52cdee1bf044cf2c1d33fa6fd1a62'

def home(request):
    return render(request, 'home.html')
"""
def crypto_to_crypto(request):
    if request.method == 'POST':
        from_currency = request.POST['from_currency']
        to_currency = request.POST['to_currency']
        amount = request.POST['amount']
        
        api_url = f'http://api.coinlayer.com/convert?access_key={API_KEY}&from={from_currency}&to={to_currency}&amount={amount}'
        
        data = requests.get(api_url).json()
        print("Data", data)
        result = data['result']
        print("data['result']", data['result'])
        
        context = {'result': result}
        
        return render(request, 'crypto-rates/crypto_to_crypto.html', context)

    currencies = ['BTC', 'ETH', 'XRP'] # etc
    
    context = {'currencies': currencies}
    
    return render(request, 'crypto-rates/crypto_to_crypto.html', context)

def crypto_to_currency(request):
    # Similiar logic as above
    pass
    
"""
# crypto_prices/views.py
from django.shortcuts import render
import requests

def crypto_prices(request):
    if request.method == 'POST':
        selected_cryptos = request.POST.getlist('cryptos')
        selected_currencies = request.POST.getlist('currencies')

        api_key = "337c9a5f7c2dadc3d6eb76ef6d162c129fb7bc6e1babb105d4e695168df0355a"
        prices = {}

        for crypto in selected_cryptos:
            url = f'https://min-api.cryptocompare.com/data/price?fsym={crypto}&tsyms={",".join(selected_currencies)}&api_key={api_key}'
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                prices[crypto] = data
            else:
                prices[crypto] = {'error': 'Unable to fetch data'}

        return render(request, 'crypto_prices/result.html', {'prices': prices})

    return render(request, 'crypto_prices/crypto_prices_form.html')

# views.py

from django.shortcuts import render

def careers(request):
    job_profiles = [
        {
            'title': 'Blockchain Developer',
            'description': 'Join our innovative blockchain development team to create decentralized applications and smart contracts. Bring expertise in blockchain technologies, such as Solidity, and contribute to shaping the future of digital finance.',
            'requirements': 'Experience with smart contract development, Solidity, etc.',
            #'recruiter_email': 'recruiter@cryptocurrency.com',
        },
        {
            'title': 'Cryptocurrency Analyst',
            'description': 'Be a key player in our analytics team, analyzing cryptocurrency trends, market behavior, and providing insights to guide investment decisions. Utilize your analytical skills to interpret complex data and contribute to strategic decision-making.',
            'requirements': 'In-depth knowledge of cryptocurrency markets, data analysis skills.',
            #'recruiter_email': 'analyst_recruiter@cryptocurrency.com',
        },
        {
            'title': 'UI/UX Designer',
            'description': 'Envision and craft exceptional user experiences for our cryptocurrency platform. Collaborate with cross-functional teams to design intuitive interfaces, ensuring a seamless and visually appealing journey for our users.',
            'requirements': 'Proven experience in designing user interfaces for fintech applications.',
            #'recruiter_email': 'design_recruiter@cryptocurrency.com',
        },
        # {
        #     'title': 'Security Engineer',
        #     'description': 'Safeguard our digital assets by taking a lead role in developing and implementing robust security measures. Work on threat detection, vulnerability assessments, and security protocols to ensure the integrity and confidentiality of our systems.',
        #     'requirements': 'Expertise in blockchain security, cryptography, and secure coding practices.',
        #     #'recruiter_email': 'security_recruiter@cryptocurrency.com',
        # },
        # {
        #     'title': 'Finance Manager',
        #     'description': 'Manage financial operations for our cryptocurrency ventures. Oversee budgeting, financial planning, and reporting, providing strategic insights to support business growth. Bring expertise in financial analysis, risk management, and compliance.',
        #     'requirements': 'Experience in financial management, accounting, and regulatory compliance.',
        #     #'recruiter_email': 'finance_recruiter@cryptocurrency.com',
        # },
        # {
        #     'title': 'Marketing Specialist',
        #     'description': 'Drive the marketing strategy for our cryptocurrency products, creating engaging campaigns and content. Utilize your skills in digital marketing, social media, and branding to enhance our market presence and attract a broader audience.',
        #     'requirements': 'Proven track record in cryptocurrency marketing and social media promotion.',
        #     #'recruiter_email': 'marketing_recruiter@cryptocurrency.com',
        # },
        # Add more job profiles as needed
    ]

    return render(request, 'careers/careers.html', {'job_profiles': job_profiles})


# views.py
# ...
# views.py
"""
import requests
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os

def crypto_chart(request):
    api_key = 'LH3X31BY3QOA1PDV'
    
    if request.method == 'POST':
        crypto_symbol = request.POST.get('crypto_symbol')
        chart_interval = request.POST.get('chart_interval')

        api_url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_{chart_interval}&symbol={crypto_symbol}&market=CNY&apikey={api_key}'
        
        response = requests.get(api_url)
        data = response.json()
        print("Data:- ",data)

            # ...

       # ...

        try:
            # Extract data and generate a simple plot (for illustration purposes)
            # In a real application, you might want to use a more advanced plotting library
            # or create more complex visualizations based on the data structure returned by the API.
            
            # Extract the time series data
            time_series_data = data.get('Time Series (Digital Currency Daily)', {})
            
            # Extract dates and prices from the time series data
            dates = list(time_series_data.keys())
            prices = [float(time_series_data[date]['4a. close (CNY)']) for date in sorted(dates, reverse=True)]

            plt.plot(dates, prices)
            plt.title(f'{crypto_symbol} Daily Prices')
            plt.xlabel('Date')
            plt.ylabel('Price (CNY)')
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Save the plot to a temporary file
            plot_file_path = 'C:/Users/rahul/Downloads/Internet Application Project/COMP8347-Internet-Application-Distributed-System/myApp/crypto_plot.png'
            plt.savefig(plot_file_path)
            plt.close()

            # Log the values to a text file
            log_values(response, data, prices, dates)

            # Pass the plot file path to the template
            return render(request, 'crypto_chart.html', {'plot_file_path': plot_file_path})

        except KeyError as e:
            error_message = f"KeyError: {e}. The data structure might have changed."
            return render(request, 'crypto_chart.html', {'error_message': error_message})


            
    return render(request, 'crypto_chart.html')
# C:/Users/rahul/Downloads/Internet Application Project/COMP8347-Internet-Application-Distributed-System/myApp/crypto_plot.png
# ...
"""
import requests
from django.shortcuts import render
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def crypto_chart(request):
    api_key = 'WW843ZFVH3MLIUBT'

    if request.method == 'POST':
        crypto_symbol = request.POST.get('crypto_symbol')
        chart_interval = request.POST.get('chart_interval')

        api_url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_{chart_interval}&symbol={crypto_symbol}&market=CNY&apikey={api_key}'

        response = requests.get(api_url)
        data = response.json()
        print("API Response Data:", data)  # Add this line for debugging

        try:
            # Extract data and generate a simple Plotly plot
            time_series_data = data.get('Time Series (Digital Currency Daily)', {})
            print("time_series_data:", time_series_data)  # Add this line for debugging

            dates = list(time_series_data.keys())
            prices = [float(time_series_data[date]['4a. close (CNY)']) for date in sorted(dates, reverse=True)]

            # Create a Plotly subplot
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            # Add a trace for the prices
            fig.add_trace(go.Scatter(x=dates, y=prices, name='Price (CNY)', mode='lines'))

            # Update layout
            fig.update_layout(title=f'{crypto_symbol} Daily Prices',
                              xaxis_title='Date',
                              yaxis_title='Price (CNY)',
                              xaxis=dict(tickangle=45),
                              showlegend=True)

            # Pass the plot to the template
            plot_div = fig.to_html(full_html=False)
            return render(request, 'crypto_chart.html', {'plot_div': plot_div})

        except KeyError as e:
            error_message = f"KeyError: {e}. The data structure might have changed."
            return render(request, 'crypto_chart.html', {'error_message': error_message})

    return render(request, 'crypto_chart.html')

def log_values(response, data, prices, dates):
    # Log the values to a text file (append mode)
    print("dates:- ", dates)
    log_file_path = 'crypto_log.txt'
    with open(log_file_path, 'a') as log_file:
        log_file.write("Response:\n")
        log_file.write(str(response) + '\n\n')

        log_file.write("Data:\n")
        log_file.write(str(data) + '\n\n')

        log_file.write("Prices:\n")
        log_file.write(str(prices) + '\n\n')

        log_file.write("Dates:\n")
        log_file.write(str(dates) + '\n\n')

from django.shortcuts import render
import requests
from django.http import JsonResponse

# Add these import statements at the top of your views.py
from django.shortcuts import render
from django.http import JsonResponse

# Your existing functions

# cryptoapp/views.py
from django.shortcuts import render
import requests
from django.http import JsonResponse
# cryptoapp/views.py
from django.shortcuts import render
import requests
from django.http import JsonResponse

# cryptoapp/views.py
from django.shortcuts import render
import requests
import plotly.graph_objects as go
from django.http import JsonResponse

def get_crypto_data(request):
    if request.method == 'POST':
        pair_type = request.POST.get('pair_type', 'histoday')
        crypto = request.POST.get('crypto', 'BTC')
        currency = request.POST.get('currency', 'USD')
        limit = request.POST.get('limit', 10)

        api_key = '337c9a5f7c2dadc3d6eb76ef6d162c129fb7bc6e1babb105d4e695168df0355a'
        url = f'https://min-api.cryptocompare.com/data/v2/{pair_type}?fsym={crypto}&tsym={currency}&limit={limit}&api_key={api_key}'
        response = requests.get(url)
        data = response.json()['Data']['Data']
        print("RESPONSE:- ", response)
        print(data)
        labels = [entry['time'] for entry in data]
        close_prices = [entry['close'] for entry in data]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=labels, y=close_prices, mode='lines', name='Close Prices'))

        fig.update_layout(
            title='Crypto Prices',
            xaxis_title='Time',
            yaxis_title='Close Price',
            xaxis=dict(type='date'),
        )

        return JsonResponse({'plot': fig.to_html()})
    
    return render(request, 'registration/hist_data.html')
