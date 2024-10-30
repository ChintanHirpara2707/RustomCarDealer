# accounts/forms.py
from django import forms

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True, label='OTP')
    new_password = forms.CharField(widget=forms.PasswordInput, required=True, label='New Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, label='Confirm New Password')

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("The two password fields must match.")
