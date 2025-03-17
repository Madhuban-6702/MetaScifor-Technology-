from django import forms
from .models import CustomUser, Booking

class SignupForm(forms.ModelForm):
    full_name = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ["username", "full_name", "email", "phone_number", "password"]

class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label="New Password")

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'number_of_people']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'number_of_people': forms.NumberInput(attrs={'min': 1}),
        }