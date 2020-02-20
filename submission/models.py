from django.db import models
from assignment.models import Assignment
from account.models import User
import uuid


STATUS_CHOICE = (
    (-1, 'Submitted'),
    (0, 'Accepted'),
    (1, 'Rejected'),
)

STATUS_STR = {
    -1: 'Submitted',
    0: 'Accepted',
    1: 'Rejected',
}

class SubmissionStatus(object):
    SUBMITTED = -1
    ACCEPTED = 0
    REJECTED = 1

# upload file rename
def submit_pdf_upload_to(instance, filename):
        # submit_authoer.name name assignment.title
        return 'pdf/submission/{assignment_id}/{name}_{title}.{filename_ext}'.format(
            assignment_id=instance.assignment.id,
            name=instance.submit_author.name,
            title=instance.assignment.title,
            filename_ext=filename.split('.')[-1]
        )

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICE, db_index=True, default=SubmissionStatus.SUBMITTED)

    submit_author = models.ForeignKey(User, on_delete=models.CASCADE)
    submit_time = models.DateTimeField(auto_now_add=True)
    submit_content = models.TextField(blank=True)
    submit_pdf = models.FileField('提交pdf', upload_to=submit_pdf_upload_to, null=True, blank=True)
    
    feedback_auther = models.ManyToManyField(User, related_name='submission_feedback_author', blank=True)
    feedback_time = models.DateTimeField(null=True, blank=True)
    feedback_score = models.IntegerField(null=True, blank=True, default=100)
    feedback_content = models.TextField(blank=True)
    feedback_pdf = models.FileField('反馈pdf', upload_to='pdf/%Y%m%d/', null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.submit_author, self.assignment)

    def get_last_submission(self, user_id, assignment_id):
        last_submission = self.objects.filter(submit_author=user_id, 
            assignment=assignment_id).order_by('-submit_time').first()
        if last_submission == None:
            return None
        return {
            'pk': last_submission.pk, 
            'status': STATUS_STR[last_submission.status],
        }
