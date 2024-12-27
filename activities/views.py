from django.shortcuts import render, redirect  # Ensure render is imported
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView
from django.forms import ModelForm
from .forms import SubmissionForm,ActivityForm,GradingRubricFormSet
from .models import Activity, Submission
from django.utils.timezone import now

class ActivityCreateView(CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'activities/activity_form.html'
    success_url = reverse_lazy('activities:activity_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['rubric_formset'] = GradingRubricFormSet(self.request.POST)
        else:
            context['rubric_formset'] = GradingRubricFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        rubric_formset = context['rubric_formset']
        if rubric_formset.is_valid():
            self.object = form.save()
            rubrics = rubric_formset.save(commit=False)
            for rubric in rubrics:
                rubric.activity = self.object
                rubric.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

# List all Activities
class ActivityListView(ListView):
    model = Activity
    template_name = 'activities/activity_list.html'
    context_object_name = 'activities'


# Show details of an Activity
class ActivityDetailView(DetailView):
    model = Activity
    template_name = 'activities/activity_detail.html'
    context_object_name = 'activity'




class SubmissionCreateView(CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = 'activities/upload_submission.html'

    def form_valid(self, form):
        # Ensure the related activity is correctly set
        activity = get_object_or_404(Activity, pk=self.kwargs['pk'])
        form.instance.activity = activity
        form.instance.submission_time = now()
        return super().form_valid(form)

    def get_success_url(self):
        # Ensure the success URL includes the correct activity PK
        return reverse_lazy('activities:activity_detail', kwargs={'pk': self.kwargs['pk']})
