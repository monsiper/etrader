from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from forms import LoginForm, SignupForm


# user login view
def login_user(request):

    if request.method == 'POST':
        processed_data = LoginForm(request.POST)
        if processed_data.is_valid():
            login(request, processed_data.cleaned_user)
            return redirect(reverse('dashboard'))
        else:
            return render(request, "user_login/login_or_signup.html", {'header': 'Login', 'form': processed_data})
    else:
        empty_Form = LoginForm()
        return render(request, "user_login/login_or_signup.html", {'header': 'Login', 'form': empty_Form})



#user signup view

def signup_user(request):
    # if uer is logged in , rediret to dashboard
    if request.method == 'POST':
        processed_data = SignupForm(request.POST)
        if processed_data.is_valid():
            first_name = processed_data.cleaned_data['first_name']
            last_name = processed_data.cleaned_data['last_name']
            email = processed_data.cleaned_data['email']
            password = processed_data.cleaned_data['password']

            with transaction.atomic():
                User.objects.create_user(first_name=first_name, last_name=last_name,
                                         username=email, email=email, password=password)

            user = authenticate(username=email, password=password)
            login(request, user)
            return redirect(reverse('dashboard'))
        else:
            return render(request, "user_login/login_or_signup.html", {'header': 'Sign Up', 'form': processed_data})
    else:
        empty_Form = SignupForm()
        return render(request,"user_login/login_or_signup.html", {'header': 'Sign Up', 'form': empty_Form})

def logout_user(request):
    logout(request)
    return redirect(reverse('main_page'))


# def main_page(request):
#
#     if request.user.is_authenticated():
#         return render(request,"user_login/main.html")
#         # do something for logged in user
#     else:
#         pass
#         # do something for logged out user
#     return HttpResponse("OK")