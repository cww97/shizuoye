from django.contrib import admin
from django.urls import path, include
from .views import AssignmentListView, AssignmentDetailView
from submission.views import submit_assignment


urlpatterns = [
    path('', AssignmentListView.as_view(), name='assignment_list'),
    # path('<int:pk>/', AssignmentDetailView.as_view(), name='assignment_detail'),
    path('<int:pk>/', submit_assignment, name='assignment_detail'),
]
