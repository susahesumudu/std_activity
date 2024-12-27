from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import Group, User
from django.views.generic import TemplateView, ListView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging
import joblib  # Assuming you're using a pre-trained model saved with joblib
import pandas as pd
import os
from django.conf import settings
from django.core.mail import send_mail


def sendmail():
    send_mail(
                subject='Your Final Grade Prediction',
                message=f'Dear {marks_tracker.student.first_name},\n\n'
                        f'Your final grade has been predicted as: {grade}. '
                        f'Please check the dashboard for more details.\n\n'
                        'Best regards,\nYour School Team',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[student_email],
                fail_silently=False,
            )


# Initialize logger
logger = logging.getLogger(__name__)

# Define normalize_input function
def normalize_input(input_data):
    """Normalize input data using the fitted scaler."""
    scaler_path = os.path.join(settings.BASE_DIR, 'users/models/scaler_vdataset.pkl')
    scaler = joblib.load(scaler_path)

    # Make sure these match the features used during model training
    columns = ['gender', 'num_of_prev_attempts', 'final_assessment_score', 
               'tasks_completed', 'practical_hours', 'theory_hours', 
               'exercises_completed', 'industry_training_experience']
    input_df = pd.DataFrame(input_data, columns=columns)
    return scaler.transform(input_df)



# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'users/login.html'  # Path to your custom login template

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return reverse_lazy('admin:index')  # Redirect admin to admin site
        elif user.groups.filter(name='Student').exists():
            return reverse_lazy('student_dashboard')
        elif user.groups.filter(name='Teacher').exists():
            return reverse_lazy('teacher_dashboard')
        elif user.groups.filter(name='Staff').exists():
            return reverse_lazy('staff_dashboard')
        else:
            return reverse_lazy('default_dashboard')  # Redirect regular users to their home page





# Home View for Regular Users
class UserHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'user_home.html'  # Regular user home page
    login_url = 'login'  # Redirect if the user is not logged in


# Student Dashboard
class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'student_dashboard.html'
    login_url = 'login'  # Redirect to login if not authenticated



# Teacher Dashboard
class TeacherDashboardView(LoginRequiredMixin, ListView):
    template_name = 'teacher_dashboard.html'
    login_url = 'login'
    
    
   
# Staff Dashboard
class StaffDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'staff_dashboard.html'
    login_url = 'login'


# Profile View Example
class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = 'Nina Mcintire'
        context['followers'] = 1322
        context['following'] = 543
        context['friends'] = 13287
        context['education'] = 'B.S. in Computer Science from the University of Tennessee at Knoxville'
        context['location'] = 'Malibu, California'
        context['skills'] = ['UI Design', 'Coding', 'Javascript', 'PHP', 'Node.js']
        context['notes'] = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        return context

