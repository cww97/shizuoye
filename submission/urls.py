from django.urls import path
from .views import SubmissionListView, SubmissionDetailView, submit_assignment

urlpatterns = [
    path('', SubmissionListView.as_view(), name='submission_list'),
    path('<str:pk>/', SubmissionDetailView.as_view(), name='submission_detail'),
]