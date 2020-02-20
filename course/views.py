from django.shortcuts import render
from django.views import generic
from .models import Course
from django.views.generic import ListView, DetailView, FormView

class CourseListView(ListView):
    model = Course
    template_name = 'course/list.jinja2'
    context_object_name = 'courses'

    def get_queryset(self):
        return self.model.objects.order_by('-create_time')

class CourseDetailView(DetailView):
    model = Course
    template_name = 'course/detail.jinja2'
    context_object_name = 'course'
    def get_queryset(self):
        return self.model.objects

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx