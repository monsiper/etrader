from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User



class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30,
                                 label='First Name',
                                 required=True)
    last_name = forms.CharField(max_length=30,
                                label='Last Name',
                                required=True)
    email = forms.EmailField(label='Email',
                             required=True)
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput,
                               required=True)

    #def clean_email():
    #def clean_first_name():

    def clean_email(self):
        return self.cleaned_data['email'].lower().strip()

    def clean(self):
        super(SignupForm, self).clean()
        if 'email' in self.cleaned_data:
            email_data = self.cleaned_data['email']
            if User.objects.filter(username=email_data).exists():
                raise forms.ValidationError('A user with the same email address already exists in the platform')


class LoginForm(forms.Form):
    email = forms.EmailField(required=True,
                             label='Email')
    password = forms.CharField(widget=forms.PasswordInput,
                               required=True,
                               label='Password')

    def clean(self):
        super(LoginForm, self).clean()

        if 'email' in self.cleaned_data and 'password' in self.cleaned_data:

            email_data = self.cleaned_data['email']
            password_data = self.cleaned_data['password']
            user = authenticate(username=email_data, password=password_data)

            if user is None:
                raise forms.ValidationError("We could not authenticate")
            else:
                self.cleaned_user = user

