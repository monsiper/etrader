from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from forms import LoginForm, SignupForm


# user login view
def login_user(request):

    if request.method == 'POST':
        processed_data = LoginForm(request.POST)
        if processed_data.is_valid():
            email = processed_data.cleaned_data['user_name']
            password = processed_data.cleaned_data['password']
            user = User.objects.get(email=email)
            login(request, user)
            return redirect('/')
        else:
            return render(request, "user_login.html", {'form': str(processed_data.errors)})
    else:
        empty_Form = LoginForm()
        return render(request, "user_login.html", {'form': empty_Form})

#user signup view
def signup_user(request):

    if request.method == 'POST':
        processed_data = SignupForm(request.POST)
        if processed_data.is_valid():
            first_name = processed_data.cleaned_data['first_name']
            last_name = processed_data.cleaned_data['last_name']
            email = processed_data.cleaned_data['email']
            password = processed_data.cleaned_data['password']
            user = User.objects.create(first_name=first_name, last_name=last_name,
                                       username=email, email=email, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, "user_sign_up.html", {'form': str(processed_data.errors)})
    else:
        empty_Form = SignupForm
        return render(request,"user_signup.html", {'form': empty_Form})


