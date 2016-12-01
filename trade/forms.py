from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import decimal


class TradeForm(forms.Form):
    num_of_coins = forms.DecimalField(max_digits=7,
                                      decimal_places=2,
                                      label='Num of Coins',
                                      required=True)

    amount = forms.DecimalField(max_digits=8,
                                decimal_places=2,
                                label='Amount')

    def clean(self):
        super(TradeForm, self).clean()
        if 'num_of_coins' in self.cleaned_data:
            num_of_coins = self.cleaned_data['num_of_coins']
            if num_of_coins <= decimal.Decimal(0.0):
                raise forms.ValidationError('Number of coins has to be greatet than zero')
