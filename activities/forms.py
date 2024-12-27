from django import forms
from .models import Submission, Activity, GradingRubric

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['activity', 'student', 'submission_file', 'marks', 'feedback']

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'description', 'instructions', 'duration_minutes']

GradingRubricFormSet = forms.inlineformset_factory(
    Activity,
    GradingRubric,
    fields=('criteria', 'excellent_description', 'good_description', 'average_description', 'poor_description', 'weight'),
    extra=1,  # Allow adding one grading criterion by default
    can_delete=True  # Allow deletion of grading criteria
)

class ScoringForm(forms.Form):
    instruction_id = forms.IntegerField(widget=forms.HiddenInput())
    marks_awarded = forms.IntegerField()

from .models import Question

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        for question in questions:
            choices = [(choice.id, choice.text) for choice in question.choices.all()]
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect,
                label=question.text
            )
