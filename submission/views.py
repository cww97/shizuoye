from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import ListView, DetailView
from .models import Submission, SubmissionStatus, STATUS_STR
from .forms import SubmitAssignmentForm, FeedbackAssignmentForm
from assignment.models import Assignment
from django.http import HttpResponseRedirect
from django.urls import reverse
from account.models import User


class SubmissionListView(ListView):
    model = Submission
    template_name = 'submission/list.jinja2'
    # paginate_by = 100
    context_object_name = 'submissions'
    
    def get_ordering(self):
        return "-submit_time"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['STATUS_STR'] = STATUS_STR
        return context


class MySubmissionListView(SubmissionListView):
    template_name = 'submission/my_submissions.jinja2'
    
    def get_queryset(self, **kwargs):
        user = self.request.GET.get('user')
        queryset = super().get_queryset(**kwargs)
        return queryset.filter(submit_author=user)


class SubmissionDetailView(DetailView):
    """
    show the detail of a submission, assert one submission has content or
    pdf file, if content, render the markdown, if pdf, preview it(or show 
    the file at first). If its status is just 'submitted', ok.

    if the teacher gave the feedback, show the feedback details includes:
    status: Accept/Reject, score, feedback content/pdf
    """
    model = Submission
    template_name = 'submission/detail.jinja2'
    context_object_name = 'submission'

    def get_queryset(self):
        return self.model.objects


# create or update a submission
def submit_assignment(request, pk):
    if request.method == 'POST':
        form = SubmitAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            ## 这里check一下用户的真实姓名有没有填吧，如果没用填弹出提示信息
            #
            #
            #
            #
            ###########################################################

            instance = Submission.objects.get_or_create(
                assignment=get_object_or_404(Assignment, pk=pk),
                submit_author=request.user,
                status = SubmissionStatus.SUBMITTED,
            )[0]
            instance.submit_content = form.cleaned_data.get('submit_content')
            instance.submit_pdf = form.cleaned_data.get('submit_pdf')
            instance.save()
            return redirect(reverse('submission_detail', kwargs={'pk': instance.pk}))
    
    my_submissions = Submission.objects.filter(submit_author=request.user.id, 
            assignment=pk).order_by('-submit_time')
    ctx = {
        'form': SubmitAssignmentForm(),
        'assignment': get_object_or_404(Assignment, pk=pk),
        'STATUS_STR': STATUS_STR,
        'submissions': my_submissions,
        'last_submission': my_submissions.first(),
    }
    return render(request, 'assignment/detail.jinja2', ctx)
