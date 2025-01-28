from django import forms
from store.models import User,Order
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]


class LoginForm(forms.Form):
   username = forms.CharField( widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),label='Username')   
   password= forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        label='Password'
    )


class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=["address","phone","payment_method"]
         