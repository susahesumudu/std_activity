from django.urls import path
from .views import SignupView, LoginView, LogoutView, EmailVerificationView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/<uidb64>/<token>/', EmailVerificationView.as_view(), name='verify_email'),
]

