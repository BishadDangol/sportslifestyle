from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput)
    email = forms.CharField(widget=forms.TextInput, )
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('username', 'email', 'password', 'contact')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Customer.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email
