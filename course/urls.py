from django.contrib import admin
from django.urls import path, include
from .views import CourseListView, CourseDetailView


urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
]
