from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django import forms
from user_login.forms import LoginForm
# Create your views here.

class TestForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'required': True, 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True, 'class': 'form-control'}))


def main_page(request):
    if request.user.is_authenticated():
        return redirect(reverse('dashboard'))
    return render(request, 'main_page.html')


def user_panel(request, type='dashboard'):
    if not request.user.is_authenticated():
        empty_Form = LoginForm()
        return render(request, "user_login/login_or_signup.html", {'header': 'Login', 'form': empty_Form}, status=403)

    return render(request, 'user_panel.html', {'parent_page': type})

