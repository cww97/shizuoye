from django.forms import ModelForm
from .models import Submission
from django.shortcuts import get_object_or_404
from assignment.models import Assignment
from django.core.exceptions import NON_FIELD_ERRORS



class SubmitAssignmentForm(ModelForm):
    class Meta:
        model = Submission
        fields = ['submit_content', 'submit_pdf']
        # error_messages = {'username': {'require': "请输入用户名。"},}

    def is_valid(self):
        if not super().is_valid():
            return False
        ctx = self.cleaned_data.get('submit_content')
        pdf = self.cleaned_data.get('submit_pdf')
        # assert False
        if ctx == '' and pdf ==None:
            self.add_error(NON_FIELD_ERRORS, '您想交白卷吗')
            # add 了 error, 不过前端没有显示，天亮再管把
            #
            #
            #
            ##########################################
            return False
        return True


class FeedbackAssignmentForm(ModelForm):
    class Meta:
        model = Submission
        fields = ['feedback_content', 'feedback_score', 'feedback_score']



'''
    def create(self):
        instance = self.save(commit=False)
        instance.set_password(self.cleaned_data.get('password'))
        if not User.objects.exists():
            instance.is_superuser = True
        instance.save()
        return instance

    def clean(self):
        data = super(RegisterForm, self).clean()
        if data.get('password') != data.get('repeat_password'):
            self.add_error('repeat_password', forms.ValidationError("密码不匹配。", code='invalid'))
        return data
'''