from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=320, label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=255, label="Username", widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=255, label="Nome", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=255, label="Cognome", widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=15, label="Numero di telefono", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    birth_date = forms.DateField(label="Data di nascita", widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), required=False)

    class Meta:
        model = CustomUser
        fields = ("email", "username", "first_name", "last_name", "phone_number", "birth_date", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
