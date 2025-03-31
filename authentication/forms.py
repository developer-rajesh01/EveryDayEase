# forms.py
from django import forms
from authentication.models import Feedback,ContactServices
from allauth.account.forms import SignupForm
from .models import ShopkeeperProfile
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()
# from django_recaptcha.fields import ReCaptchaField
# from django_recaptcha.widgets import ReCaptchaV2Checkbox
# -------------------------------------------------------------------------------------------------



class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['content', 'rating','real']

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your feedback content (e.g., product or post)',
                'rows': 4,
                'required':False
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'content': 'Feedback Message',
            'rating': 'Rating (1 to 5)',
        }

    # Custom validation (optional)
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactServices
        fields = ['name','email','subject','message']

        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your message...',
                'rows': 9,
                'cols':25,
                'required':True
            }),
            'subject': forms.Select(attrs={
                'class': 'form-select',
            }),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
            'name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),

        }


class ShopkeeperRegistrationForm(forms.ModelForm):
    class Meta:
        model = ShopkeeperProfile
        fields = [
            'business_name', 'email', 'country_code', 'phone',
            'service_type', 'specializations', 'experience', 'certification', 'certification_file',
            'opening_time', 'closing_time',
            'street', 'city', 'state', 'pincode',
            'aadhar_number', 'aadhar_file', 'profile','gst_number',
            'payment_type', 'individual_name', 'account_number', 'ifsc_code', 'upi_id'
        ]

        widgets = {
            # 'fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Full Name'}),
            'business_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Business Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'country_code': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'service_type': forms.Select(attrs={'class': 'form-select'}),
            'specializations': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Enter Experience in Years'}),
            'certification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Certification Name'}),
            'certification_file': forms.FileInput(attrs={'class': 'form-control'}),
            'opening_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Street'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter State'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter PIN Code'}),
            'aadhar_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Aadhar Number'}),
            'aadhar_file': forms.FileInput(attrs={'class': 'form-control'}),
            'profile': forms.FileInput(attrs={'class': 'form-control'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter GST number (Optional)'}),
            'payment_type': forms.Select(attrs={'class': 'form-select'}),
            'individual_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Account Holder Name'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Account Number'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter IFSC Code'}),
            'upi_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter UPI ID'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) < 10 or len(phone) > 15:
            raise forms.ValidationError("Enter a valid phone number (10-15 digits).")
        return phone

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if not pincode.isdigit() or len(pincode) != 6:
            raise forms.ValidationError("Enter a valid 6-digit PIN code.")
        return pincode

    def clean_aadhar_number(self):
        aadhar_number = self.cleaned_data.get('aadhar_number')
        if not aadhar_number.isdigit() or len(aadhar_number) != 12:
            raise forms.ValidationError("Enter a valid 12-digit Aadhar number.")
        return aadhar_number


class ProfileRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False,widget=forms.EmailInput(attrs={"placeholder":"Email address"}))  # Optional email field
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"})
    )


    class Meta:
        model = Profile  # Use your custom Profile model
        fields = ["username", "email", "password1", "password2"]

        widgets = {
            "username":forms.TextInput(attrs={"placeholder":"username"})
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)  # Create user object but don't save yet
        if commit:
            user.set_password(self.cleaned_data["password1"])  # Hash password
            user.save()  # Now save the user
        return user