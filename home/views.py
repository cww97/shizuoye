from django.shortcuts import render
from django.http import HttpResponse
from course.models import Course
from account.models import User
from sortask.settings import MEDIA_URL

def home_view(request):
    # return HttpResponse("Hello, world. You're at the index.")
    if request.user.is_authenticated:
        
        ctx = {
            'courses': Course.objects.order_by('create_time')[:10],
            'joined_courses': User.objects.get(id=request.user.pk).course_participants.all().order_by('create_time')[:5]
        }
        return render(request, 'home/home.jinja2', context = ctx)
    else:
        return render(request, 'home/welcome.jinja2')