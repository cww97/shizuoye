from django.forms import Form, IntegerField, ModelForm
from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from captcha.fields import CaptchaField
from django.utils.translation import ugettext_lazy as _


class LoginForm(AuthenticationForm):
    captcha = CaptchaField(label="小学数学题")
    remember_me = forms.BooleanField(label="记住我", required=False)

    error_messages = {
        'invalid_login': _(
        "请输入正确的用户名和密码。注意区分大小写。"
        ),
        'inactive': "该账户已失效。",
    }

    def __init__(self, request=None, *args, **kwargs):  # pylint: disable=keyword-arg-before-vararg
        super(LoginForm, self).__init__(request, *args, **kwargs)
        self.fields['username'].label = "用户名或手机号"
        self.fields['password'].label = "密码"

    def clean(self):
        username = self.cleaned_data.get('username')
        users = User.objects.filter(phone='+86'+username)
        if len(users):
            username = users[0].username
            self.cleaned_data['username'] = username
        return super().clean()


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['phone', 'username']
        error_messages = {
            'username': {
                'require': "请输入用户名。"
            },
            'phone': {
                'require': "请输入手机号"
            }
        }

    password = forms.CharField(help_text="至少六位",
                                widget=forms.PasswordInput,
                                min_length=6,
                                required=True,
                                error_messages={
                                    'min_length': "密码太短",
                                    'require': "请输入密码。"
                                },
                                label=("密码"))
    repeat_password = forms.CharField(widget=forms.PasswordInput,
                                required=True,
                                error_messages={
                                    'require': "请重复输入密码。"
                                },
                                label="确认密码")
    captcha = CaptchaField(label="验证码")

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
