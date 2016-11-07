from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django import forms
# Create your views here.

class TestForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'required': True, 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True, 'class': 'form-control'}))


def main_page(request):
    return render(request, 'main_page.html')


def dashboard(request):
    if not request.user.is_authenticated():
        return redirect(reverse('login'))

    return render(request, 'dashboard.html', {'username': request.user.username})