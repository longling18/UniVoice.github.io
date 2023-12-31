from django import forms
from projectapp.models import CustomUser 
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth.forms import AuthenticationForm
from .models import FeedbackProvider, FeedbackEntry

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    otp_token = forms.CharField(label='OTP_Token', required=False)

class CustomLoginForm(AuthenticationForm):
    captcha = ReCaptchaField()
    otp_token = forms.CharField(label='OTP Token', required=False) 

    def clean(self):
        cleaned_data = super().clean()
        captcha_value = cleaned_data.get("captcha")

        if not captcha_value:
            self.add_error('captcha', 'Please check the reCAPTCHA box to continue.')

        return cleaned_data

'''
class Signup(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Password don\'t match.')
        return cd['password2']
'''
class StaffAddForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'profile_image']

class FeedbackEntryForm(forms.ModelForm):
    class Meta:
        model = FeedbackEntry
        fields = ['feedback', 'feedback_image', 'category', 'building']

class SubmitForm(forms.ModelForm):
    is_anonymous = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput(),
        initial=False
    )
    building_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True,
    )
    category_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True,
    )

    class Meta:
        model = FeedbackProvider
        fields = ['first_name', 'last_name', 'college', 'is_anonymous']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data