from django.contrib.auth import login
from django.shortcuts import render, redirect
from forms import SignupForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from forms import SigninForm
from django.contrib.auth import logout

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('success_view')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

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
    return redirect('signup')  # Replace 'homepage' with the name of your homepage URL pattern

def trading_view(request):
    # Your view logic here
    return render(request, 'registration/trading.html')

def livecurrencyrates_view(request):
    # Your view logic here
    return render(request, 'registration/livecurrencyrates.html')

def markettrends_view(request):
    # Your view logic here
    return render(request, 'registration/markettrends.html')



