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
