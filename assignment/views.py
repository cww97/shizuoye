from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Assignment
from course.models import Course
# from .forms import ModelFormWithFileField


class AssignmentListView(ListView):
    model = Assignment
    template_name = 'assignment/list.jinja2'
    paginate_by = 50
    context_object_name = 'dues'

    def get_queryset(self):
        return self.model.objects.order_by('-create_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for due in context['dues']:
            # attention: one assignment can only match one course 
            due.course = due.course_assignments.all()[0]
        return context


class AssignmentDetailView(DetailView):
    model = Assignment
    template_name = 'assignment/detail.jinja2'
    context_object_name = 'assignment'
    
    def get_queryset(self):
        return self.model.objects