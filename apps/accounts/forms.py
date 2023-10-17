from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ('phone_number', 'email', 'full_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('passwords dont match')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text= 'You can change password using this <a href="../password/">form</a>')

    class Meta:
        model = User
        fields = ('phone_number', 'email', 'full_name', 'password', 'last_login')


class UserRegisterationForm(forms.Form):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=11)
    full_name = forms.CharField(label='Full Name')
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email= self.cleaned_data['email']
        if User.objects.filter(email= email).exists():
            raise ValidationError('this email already exists.')
        return email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if User.objects.filter(phone_number= phone_number).exists():
            raise ValidationError('this phone number already exists.')
        return phone_number

class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()
