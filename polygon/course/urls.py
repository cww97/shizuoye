from django.urls import path
from .views import PolygonCourseListView, CourseEditView


urlpatterns = [
    path('', PolygonCourseListView.as_view(), name='course_list'),
    path('<int:pk>/', CourseEditView.as_view(), name="course_meta"), #@ polygon: course_meta
]