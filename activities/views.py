from django.shortcuts import render, redirect  # Ensure render is imported
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView
from django.forms import ModelForm
from .forms import SubmissionForm,ActivityForm,GradingRubricFormSet
from .models import Activity, Submission
from django.utils.timezone import now

from .forms import SubmissionForm
from .models import Submission


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

from django.shortcuts import render, redirect
from .models import Exercise, Submission
from .forms import SubmissionForm

def submit_exercise(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.save()
            return redirect('exercise_list')  # Replace with your exercise list page
    else:
        form = SubmissionForm()
    return render(request, 'activities/submit_exercise.html', {'form': form})

from django.shortcuts import get_object_or_404
from .models import Submission, Instruction, Score
from .forms import ScoringForm

def grade_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    instructions = submission.exercise.instructions.all()
    if request.method == 'POST':
        total_score = 0
        for instruction in instructions:
            marks_awarded = int(request.POST.get(f'marks_{instruction.id}', 0))
            total_score += marks_awarded

        Score.objects.create(submission=submission, total_score=total_score)
        submission.is_reviewed = True
        submission.save()
        return redirect('submissions_list')  # Replace with your submissions list page

    return render(request, 'grade_submission.html', {
        'submission': submission,
        'instructions': instructions,
    })


from django.shortcuts import render, get_object_or_404
from .models import Quiz, Question, Response
from .forms import QuizForm

def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            for question in questions:
                choice_id = form.cleaned_data.get(f'question_{question.id}')
                selected_choice = question.choices.get(id=choice_id)
                Response.objects.create(
                    user=request.user,
                    quiz=quiz,
                    question=question,
                    selected_choice=selected_choice
                )
            return redirect('quiz_results', quiz_id=quiz.id)
    else:
        form = QuizForm(questions=questions)

    return render(request, 'take_quiz.html', {'quiz': quiz, 'form': form})


def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    responses = Response.objects.filter(user=request.user, quiz=quiz)
    score = sum(response.selected_choice.is_correct for response in responses)
    total_questions = quiz.questions.count()
    return render(request, 'quiz_results.html', {
        'quiz': quiz,
        'score': score,
        'total_questions': total_questions
    })
