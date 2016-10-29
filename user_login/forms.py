from django import forms
from django.contrib.auth.models import User


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name', required=True)
    last_name = forms.CharField(max_length=30, label='Last Name',required=True)
    email = forms.EmailField(label='Email Address',required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput,required=True)

    #def clean_email():
    #def clean_first_name():

    def clean(self):
        super(SignupForm, self).clean()
        data = self.cleaned_data['email']
        if User.objects.filter(email__iexact=data).exists():
            raise forms.ValidationError('This username already exists in the platform')


class LoginForm(forms.Form):
    user_name = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        super(SignupForm, self).clean()
        user_name_data = self.cleaned_data['user_name']
        password_data = self.cleaned_data['password']

        if not User.objects.filter(email__iexact=user_name_data).exists() or \
                User.objects.get(email__iexact=user_name_data).password != password_data :
            raise forms.ValidationError('Make sure you entered the correct email address/password')


