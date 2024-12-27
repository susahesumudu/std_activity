
from django.urls import path
from .views import ActivityListView, ActivityDetailView, SubmissionCreateView, ActivityCreateView

app_name = 'activities'

urlpatterns = [
    path('', ActivityListView.as_view(), name='activity_list'),
    path('<int:pk>/', ActivityDetailView.as_view(), name='activity_detail'),
    path('<int:pk>/upload/', SubmissionCreateView.as_view(), name='upload_submission'),
    path('create/', ActivityCreateView.as_view(), name='activity_create'),
]
