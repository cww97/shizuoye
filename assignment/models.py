from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from account.models import User


class Assignment(models.Model):

    title = models.CharField(_('Title'), max_length=192, blank=True)
    description = models.TextField("描述", blank=True)

    start_time = models.DateTimeField("开始时间", blank=True, null=True, default=timezone.now)
    end_time = models.DateTimeField("结束时间", blank=True, null=True, default=timezone.now)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    # who create this assignment
    author = models.ForeignKey(User, related_name='assignment_author', on_delete=models.CASCADE)

    pdf_statement = models.FileField('PDF说明', upload_to='pdf/%Y%m%d/', null=True, blank=True)

    def __str__(self):
        return self.title
