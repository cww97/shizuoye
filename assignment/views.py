from django.shortcuts import render, reverse
from django.views.generic import ListView, DetailView
from .models import Assignment
# from .forms import ModelFormWithFileField


class AssignmentListView(ListView):
    model = Assignment
    template_name = 'assignment/list.jinja2'
    # paginate_by = 100
    context_object_name = 'dues'

    def get_queryset(self):
        return self.model.objects.order_by('-create_time')


class AssignmentDetailView(DetailView):
    model = Assignment
    template_name = 'assignment/detail.jinja2'
    context_object_name = 'assignment'
    
    def get_queryset(self):
        return self.model.objects