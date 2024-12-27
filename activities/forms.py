from django import forms
from .models import Submission
from django.forms import inlineformset_factory
from .models import Activity, GradingRubric

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'description', 'instructions', 'duration_minutes']

GradingRubricFormSet = inlineformset_factory(
    Activity,
    GradingRubric,
    fields=('criteria', 'excellent_description', 'good_description', 'average_description', 'poor_description', 'weight'),
    extra=1,  # Allow adding one grading criterion by default
    can_delete=True  # Allow deletion of grading criteria
)

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['student_name', 'uploaded_file']

