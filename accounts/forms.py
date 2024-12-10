# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nickname = forms.CharField(max_length=50, required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'nickname', 'phone_number', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('nickname', 'email', 'phone_number', 'address', 'address_detail', 'postal_code')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

class CreatorApplicationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['company_name', 'business_registration_number', 'company_description']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
