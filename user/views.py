from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm, LoginForm
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

class SignupView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'user/signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User needs email verification
            user.save()
            # Send verification email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_url = f"{request.scheme}://{request.get_host()}/user/verify/{uid}/{token}/"
            send_mail(
                'Verify your email',
                f'Click the link to verify your email: {verification_url}',
                'admin@example.com',
                [user.email],
            )
            messages.success(request, 'Signup successful! Check your email for verification.')
            return redirect('login')
        return render(request, 'user/signup.html', {'form': form})

class EmailVerificationView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.email_verified = True
            user.save()
            messages.success(request, 'Email verified successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Invalid verification link.')
            return redirect('signup')

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'userapp/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.email_verified:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Email not verified.')
                    return redirect('login')
            else:
                messages.error(request, 'Invalid credentials.')
        return render(request, 'user/login.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
