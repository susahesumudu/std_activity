from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['role'] = user.role
        if user.role == 'student':
            context['dashboard_type'] = 'Student Dashboard'
        elif user.role == 'teacher':
            context['dashboard_type'] = 'Teacher Dashboard'
        return context
