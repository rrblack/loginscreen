from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    name = forms.CharField(label= 'name', max_length=100)
    email = forms.CharField(label= 'email')

    class Meta:
        model = User
        fields = ('name', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already registered.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # hash the password
        if commit:
            user.save()
        return user
