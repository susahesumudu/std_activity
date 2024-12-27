
from django.urls import path
from .views import ActivityListView, ActivityDetailView, SubmissionCreateView, ActivityCreateView
from . import views
app_name = 'activities'

urlpatterns = [
    path('', ActivityListView.as_view(), name='activity_list'),
    path('<int:pk>/', ActivityDetailView.as_view(), name='activity_detail'),
    path('<int:pk>/upload/', SubmissionCreateView.as_view(), name='upload_submission'),
    path('create/', ActivityCreateView.as_view(), name='activity_create'),
    path('submit/', views.submit_exercise, name='submit_exercise'),
    path('grade/<int:submission_id>/', views.grade_submission, name='grade_submission'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),
]