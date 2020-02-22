from django.shortcuts import render
from django.http import HttpResponse
from course.models import Course
from account.models import User
from sortask.settings import MEDIA_URL
from assignment.models import Assignment
from django.forms.models import model_to_dict


def home_view(request):
    if request.user.is_authenticated:
        
        courses = request.user.course_participants.all()
        deadlines = Assignment.objects.none()
        for course in courses:
            objs =  course.assignments.all()
            for obj in objs:
                obj.belong_to = course
            deadlines |= objs
        deadlines = deadlines.order_by('-create_time')
        
        ctx = {
            # avatar card
            'object': request.user,
            'submission_cnt': request.user.user_submission.all().count(),

            'deadlines': deadlines,
            'joined_courses': request.user.course_participants.all().order_by('create_time')[:5]
        }
        return render(request, 'home/home.jinja2', context = ctx)
    else:
        return render(request, 'home/welcome.jinja2')