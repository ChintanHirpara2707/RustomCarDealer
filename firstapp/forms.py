from django import forms
from .models import Car
from .models import ContactMessage
from .models import CustomerReview
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['car_name', 'car_model', 'car_engine', 'car_power', 'seating_capacity', 'transmission', 'car_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['seating_capacity'].required = True

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage  # Replace with your actual model
        fields = ['email', 'phone_no', 'message']

class CustomerReviewForm(forms.ModelForm):
    class Meta:
        model = CustomerReview
        fields = ['name', 'email', 'review', 'rating']
        widgets = {
            'rating': forms.RadioSelect(),
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')