from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetDoneView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import CustomLoginForm
from django.contrib.auth.models import User

# Create your views here
def Index(request):
    return render(request, 'registration/index.html', {'section': 'index'})

def feedback_form(request):
    return render(request, 'registration/feedbackform.html', {'section': 'feedbackform'})
                  
@login_required

def mydashboard(request):
    print(request.user)
    return render(request, 'registration/dashboard.html', {'section': 'dashboard'})

class CustomLoginView(LoginView):
     form_class = CustomLoginForm  # Use the CustomLoginForm
     def form_invalid(self, form):
        # Check if the reCAPTCHA checkbox was checked
        captcha_response = form.cleaned_data.get('captcha')
        if not captcha_response:
            messages.error(self.request, 'Please check the reCAPTCHA below.')
            return super().form_invalid(form)

        # Check if the user exists in the database and the password is incorrect
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(self.request, 'Incorrect username or password. Please try again.')
            return super().form_invalid(form)

        messages.error(self.request, 'Please check the reCAPTCHA below.')
        return super().form_invalid(form)

     def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return '/admin/'  # Redirect superuser to the admin site
        else:
            return '/dashboard/'  # Redirect other users to the dashboard
def login(request):
    return render(request, 'login.html', {'section': 'login'})

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'passwordchange.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Password successfully changed.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Password change failed. Please correct the errors below.')
        return super().form_invalid(form)

def logout_user(request):
    #A message when logout
    messages.success(request, "Successfully logged out.")

    #Log out the user
    logout(request)

    #Redirect to the login html
    return redirect('login')

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

def signup(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            email = user_form.cleaned_data['email']

            # Check if an existing user with the same email address exists
            if User.objects.filter(email=email).exists():  
                messages.error(request, 'Email address is already in use.')
            else:
                # Create a new user but avoid saving it
                new_user = user_form.save(commit=False)
                # Set the chosen password
                new_user.set_password(user_form.cleaned_data['password1'])
                # Save the user object
                new_user.save()
                messages.success(request, 'Account created successfully. You can log in now.')
                return redirect('dashboard')  # Redirect to the dashboard or another page after successful signup
        else:
            # Clear existing messages
            # Add error messages for the specific form field errors with a 'signup_error' tag
            messages.error(request, 'Please correct the errors below.', 'signup_error')
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}", 'signup_error')

    else:
        user_form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'user_form': user_form})
class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_confirm.html'