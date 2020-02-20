from django.db import models
from django.utils.translation import ugettext_lazy as _
from account.models import User
from assignment.models import Assignment


class Course(models.Model):
    ACCESS_LEVEL_OPTIONS = (
        (0, '仅课程管理员可见'),
        (10, '仅受邀用户可见'),
        (20, '公开')
    )

    title = models.CharField(_('Title'), max_length=192, blank=True)
    description = models.TextField("描述", blank=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    
    access_level = models.PositiveIntegerField("访问控制", default=0, choices=ACCESS_LEVEL_OPTIONS)

    teachers = models.ManyToManyField(User, related_name='course_teacher')
    assistants = models.ManyToManyField(User, related_name='course_assistants', blank=True)

    assignments = models.ManyToManyField(Assignment, related_name='course_assignment', blank=True)
    participants = models.ManyToManyField(User, related_name='course_participants', blank=True)

    def __str__(self):
        return self.title

class CourseInvitation(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)

    class Meta:
        unique_together = ('course', 'code')